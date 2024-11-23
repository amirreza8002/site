from django.contrib.postgres.indexes import BTreeIndex
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager

from .utils import convert_pictures


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Meta:
        ordering = ["-published_at"]
        indexes = [BTreeIndex(fields=["-published_at"]), BTreeIndex(fields=["title"])]

    class Status(models.TextChoices):
        DRAFT = "D", _("Draft")
        PUBLISHED = "P", _("Published")

    title = models.CharField(verbose_name=_("title"), max_length=255)
    slug = models.SlugField(verbose_name=_("slug"), max_length=300, unique=True)
    image = models.ImageField(verbose_name=_("image"), upload_to="posts/%Y/%m/%d")
    alt = models.CharField(verbose_name=_("alt"), max_length=100)
    body = models.TextField(verbose_name=_("body"))
    status = models.CharField(
        verbose_name=_("status"),
        choices=Status.choices,
        default=Status.PUBLISHED,
        max_length=10,
    )
    created_at = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated"), auto_now=True)
    published_at = models.DateTimeField(
        verbose_name=_("published"),
        default=timezone.now,
    )

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager(
        verbose_name=_("tags"),
        blank=True,
    )
    pin = models.BooleanField(verbose_name=_("pin"), default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        new_path = convert_pictures(
            self.image.path, format="AVIF", unlink=True, pil_verify=True
        )
        self.image = str(new_path)
        super().save(
            *args,
            update_fields=["image"],
            force_update=True,
            using=kwargs.get("using", None),
        )

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"slug": self.slug})
