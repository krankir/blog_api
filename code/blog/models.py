from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# class Blog(models.Model):
#     owner = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Владелец блога",
#     )
#     posts = models.ForeignKey(
#         "Post",
#         on_delete=models.CASCADE,
#     )
#


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
    read_by_users = models.ManyToManyField(
        User,
        related_name="read_posts",
        blank=True,
    )

    class Meta:
        ordering = ["-pub_date", "author"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]
