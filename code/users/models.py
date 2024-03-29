from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    subscribed_to_newsletter = models.BooleanField(default=False)


class Follow(models.Model):
    """Модель для подписки на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following", verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(fields=["user", "author"], name="unique_follow")
        ]

    def __str__(self):
        return f"Подписчик {self.user} - автор {self.author}"
