# Generated by Django 5.1.2 on 2024-11-03 18:19

import django.contrib.postgres.indexes
import django.utils.timezone
import taggit.managers
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "slug",
                    models.SlugField(max_length=300, unique=True, verbose_name="slug"),
                ),
                ("body", tinymce.models.HTMLField(verbose_name="body")),
                (
                    "status",
                    models.CharField(
                        choices=[("D", "Draft"), ("P", "Published")],
                        default="P",
                        max_length=10,
                        verbose_name="status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated"),
                ),
                (
                    "published_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="published"
                    ),
                ),
                ("pin", models.BooleanField(default=False, verbose_name="pin")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
            ],
            options={
                "ordering": ["-published_at"],
                "indexes": [
                    django.contrib.postgres.indexes.BTreeIndex(
                        fields=["-published_at"], name="posts_post_publish_a9e525_btree"
                    ),
                    django.contrib.postgres.indexes.BTreeIndex(
                        fields=["title"], name="posts_post_title_7117c2_btree"
                    ),
                ],
            },
        ),
    ]
