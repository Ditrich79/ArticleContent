from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Article.Status.PUBLISHED)


class Article(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "PB", "Published"
        DRAFT = "DF", "Draft"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание")
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )
    publish = models.DateTimeField(
        default=timezone.now, verbose_name="Дата публикации"
    )
    status = models.CharField(
        max_length=2, choices=Status,
        default=Status.DRAFT,
        verbose_name="Статус"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="related_articles"
    )
    picture = models.ImageField(
        upload_to="articles/%Y/%m/%d/", blank=True, verbose_name="Изображение"
    )
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "article:article_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ],
        )

    class Meta:
        ordering = ["-publish"]
        verbose_name = "статью"
        verbose_name_plural = "Статьи"
        indexes = [
            models.Index(fields=["-publish"]),
        ]


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Описание"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "Категории"


class Comment(models.Model):
    name = models.CharField(max_length=90, verbose_name="Имя")
    content = models.TextField(verbose_name="Содержание")
    email = models.EmailField(verbose_name="Email")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )
    is_active = models.BooleanField(default=True)
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        indexes = [models.Index(fields=["-created"])]

    def __str__(self):
        return f"Comment by {self.name} on {self.article}."

    def get_absolute_url(self):
        return reverse("article:comment", args=[self.id])
