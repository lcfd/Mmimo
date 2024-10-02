from django.shortcuts import render
from django.forms import ModelForm
from blog.models import Post
from django_htmx.http import trigger_client_event
from django_htmx.http import HttpResponseClientRedirect
from django.template.defaultfilters import slugify

from rich import print


def view_post_public(request):
    return render(request, "base.html", {})


def posts(request):
    posts = Post.objects.filter(user=request.user)

    return render(request, "admin-posts.html", {"posts": posts})


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "markdown"]


def create_post(request):
    form = PostForm(request.POST or None)

    if request.htmx:
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data.get("title", ""))
            new_post.user = request.user
            new_post.save()
            return HttpResponseClientRedirect(f"/_/edit/{new_post.slug}")

    return render(request, "create.html", {"form": form})


def edit_post(request, id):
    # template_name = "create.html#form-partial"
    # response = render(request, template_name, {"form": form})
    # return trigger_client_event(
    #     response,
    #     "create_editor",
    #     {"content": form.cleaned_data.get("markdown", "")},
    #     after="swap",
    # )

    return render(request, "base.html", {})


def delete_post(request):
    return render(request, "base.html", {})


def preview_post(request):
    return render(request, "base.html", {})
