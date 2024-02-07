from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    title = models.CharField(
        "заголовок",
        max_length=100,
    )
    text = models.CharField(
        "Текст поста",
        max_length=140,
        help_text="Введите текст поста",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )
    is_read = models.BooleanField(
        "Прочитанное сообщение",
        default=False,
        blank=True,
    )

    class Meta:
        ordering = ["-pub_date", "author"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]
