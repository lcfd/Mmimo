import mistune
from django.forms import ModelForm, DateTimeField
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event

from blog.models import Post


def view_homepage(request):
    posts = Post.objects.filter(
        status=Post.StatusChoices.PUBLISHED,
    ).order_by("-pub_date")[:5]

    return render(request, "homepage.html", {"posts": posts})


def view_post_public(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.StatusChoices.PUBLISHED,
    )
    return render(request, "post_public.html", {"post": post})


def admin_posts(request):
    if request.user.is_superuser:
        posts = Post.objects.filter(user=request.user)

        return render(request, "admin-posts.html", {"posts": posts})

    return redirect("homepage")


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "status", "pinned", "markdown", "pub_date"]


def admin_create_post(request):
    form = PostForm(request.POST or None)

    if request.htmx:
        print(form.is_valid())
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data.get("title", ""))
            new_post.user = request.user
            new_post.html = mistune.html(form.cleaned_data.get("markdown", ""))
            new_post.save()
            return HttpResponseClientRedirect(f"/_/edit/{new_post.id}")
        else:
            response = render(request, "create.html#form-partial", {"form": form})
            response = trigger_client_event(
                response,
                "create_editor",
                {
                    "content": form.cleaned_data.get("markdown", ""),
                    "title": form.cleaned_data.get("title", ""),
                },
                after="swap",
            )
            response = trigger_client_event(
                response,
                "toast",
                {
                    "toasts": [{"kind": "error", "text": "Post not saved!"}],
                },
                after="swap",
            )
            return response

    return render(request, "create.html", {"form": form})


def admin_edit_post(request, id):
    post = get_object_or_404(Post, user=request.user, id=id)
    form = PostForm(request.POST or None, instance=post)

    if request.htmx:
        if form.is_valid():
            try:
                post: Post = form.save(commit=False)
                post.slug = slugify(form.cleaned_data.get("title", ""))
                post.html = mistune.html(form.cleaned_data.get("markdown", ""))
                post.save()
            except Exception as e:
                raise e

            template_name = "edit.html#form-partial"

            response = render(request, template_name, {"form": form, "post": post})
            response = trigger_client_event(
                response,
                "create_editor",
                {
                    "content": form.cleaned_data.get("markdown", ""),
                    "title": post.title,
                },
                after="swap",
            )
            response = trigger_client_event(
                response,
                "update_page",
                {
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
        else:
            template_name = "edit.html#form-partial"
            response = render(request, template_name, {"form": form, "post": post})
            response = trigger_client_event(
                response,
                "create_editor",
                {
                    "content": form.cleaned_data.get("markdown", ""),
                    "title": post.title,
                },
                after="swap",
            )

            response = trigger_client_event(
                response,
                "toast",
                {
                    "toasts": [{"kind": "error", "text": "Post not saved!"}],
                },
                after="swap",
            )

            return response

    return render(request, "edit.html", {"form": form, "post": post})


def admin_delete_post(request):
    return render(request, "base.html", {})


def admin_preview_post(request):
    return render(request, "base.html", {})
