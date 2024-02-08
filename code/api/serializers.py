from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from blog.models import Post
from users.models import Follow

User = get_user_model()


class PostReadMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id",)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "pub_date",
        )


class NewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "title",
            "author",
            "pub_date",
            "is_read",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class FollowSubscriptionsSerializer(serializers.ModelSerializer):
    subscriptions = SerializerMethodField()

    class Meta:
        model = User
        fields = ("subscriptions",)

    def get_subscriptions(self, obj):
        authors = obj.following.all()
        return authors


class CustomUserSerializer(UserSerializer):
    """Сериализатор просмотра пользователя."""

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для  подписки"""

    class Meta:
        model = User
        fields = ("username",)

    def validate(self, data):
        author = self.instance
        user = self.context.get("request").user
        if Follow.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail="Уже подписаны на этого пользователя!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise ValidationError(
                detail="Вы не можете подписаться сами на себя!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
