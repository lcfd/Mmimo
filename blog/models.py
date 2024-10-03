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
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    markdown = models.TextField()
    html = models.TextField()
    status = models.CharField(
        max_length=2,
        choices=StatusChoices,
        default=StatusChoices.DRAFT,
    )

    class Meta:  # ignore: type
        """Meta definition for Post."""

        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        """Unicode representation of Post."""

        return self.title
