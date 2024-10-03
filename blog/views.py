import mistune
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event

from blog.models import Post


def view_post_public(request):
    return render(request, "base.html", {})


def admin_posts(request):
    posts = Post.objects.filter(user=request.user)

    return render(request, "admin-posts.html", {"posts": posts})


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "markdown"]


def admin_create_post(request):
    form = PostForm(request.POST or None)

    if request.htmx:
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data.get("title", ""))
            new_post.user = request.user
            new_post.html = mistune.html(form.cleaned_data.get("markdown", ""))
            new_post.save()
            return HttpResponseClientRedirect(f"/_/edit/{new_post.slug}")
        else:
            return render(request, "create.html#form-partial", {"form": form})

    return render(request, "create.html", {"form": form})


def admin_edit_post(request, slug):
    post = get_object_or_404(Post, user=request.user, slug=slug)
    form = PostForm(request.POST or None, instance=post)

    if request.htmx:
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(form.cleaned_data.get("title", ""))
            post.html = mistune.html(form.cleaned_data.get("markdown", ""))
            post.save()

        template_name = "edit.html#form-partial"

        response = render(request, template_name, {"form": form, "post": post})
        response = trigger_client_event(
            response,
            "create_editor",
            {
                "content": form.cleaned_data.get("markdown", ""),
                "slug": post.slug,
                "title": post.title,
            },
            after="swap",
        )
        response = trigger_client_event(
            response,
            "update_page",
            {
                "slug": post.slug,
                "title": post.title,
            },
            after="swap",
        )

        response = trigger_client_event(
            response,
            "toast",
            {
                "toasts": [{"kind": "success", "text": "Post saved!"}],
            },
            after="swap",
        )

        return response

    return render(request, "edit.html", {"form": form, "post": post})


def admin_delete_post(request):
    return render(request, "base.html", {})


def admin_preview_post(request):
    return render(request, "base.html", {})
