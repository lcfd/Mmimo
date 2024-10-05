from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog.models import Post


def mimo_config(request):
    """Provide mimo settings to templates"""

    pinned = Post.objects.filter(
        pinned=True,
        status=Post.StatusChoices.PUBLISHED,
    )

    return {
        "MIMO_SITE_NAME": settings.MIMO_SITE_NAME,
        "MIMO_SITE_TITLE": settings.MIMO_SITE_TITLE,
        "MIMO_SITE_SUBTITLE": settings.MIMO_SITE_SUBTITLE,
        "PINNED_POSTS": pinned,
    }


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    # Mimo
    path("", include("blog.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
