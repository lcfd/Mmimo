from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin View for Post"""

    list_display = (
        "id",
        "status",
        "title",
        "slug",
        "created_date",
        "modified_date",
    )
    ordering = ("created_date",)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
