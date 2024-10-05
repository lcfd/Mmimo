from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    """Model definition for Post."""

    class StatusChoices(models.TextChoices):
        PUBLISHED = "PU", _("Published")
        DRAFT = "DR", _("Draft")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, editable=False)
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    markdown = models.TextField()
    html = models.TextField()
    pub_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=StatusChoices,
        default=StatusChoices.DRAFT,
    )
    pinned = models.BooleanField(default=False)

    class Meta:  # ignore: type
        """Meta definition for Post."""

        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        """Unicode representation of Post."""

        return self.title
