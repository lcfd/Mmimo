from django.urls import path
from blog import views

urlpatterns = [
    path("<slug:slug>", views.view_post_public, name="view-post-public"),
    # Admin
    path("_/posts", views.posts, name="admin-posts"),
    path("_/new-post", views.create_post, name="admin-create-post"),
    path("_/edit/<slug:slug>", views.edit_post, name="admin-edit-post"),
    path("_/preview/<slug:slug>", views.preview_post, name="admin-preview-post"),
]
