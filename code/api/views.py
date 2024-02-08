from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginations import CustomPagination
from api.serializers import (
    UserSerializer,
    FollowSerializer,
    NewsFeedSerializer,
    PostSerializer,
    PostReadMarkSerializer,
)
from blog.models import Post
from users.models import Follow

User = get_user_model()


class PostViewSet(viewsets.ViewSet):
    """
    Вьюсет осуществляет функционал:
    .../mark_read POST для пометки поста в ленте как прочитанного
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def mark_read(self, request, **kwargs):
        user = request.user
        post = get_object_or_404(Post, id=request.data["id"])
        serializer = PostReadMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post.read_by_users.add(user)
        post.save()
        return Response(
            {"detail": "Post marked as read."},
            status=status.HTTP_200_OK,
        )


class FollowViewSet(viewsets.ModelViewSet):
    """
    Вьюсет осуществляет функционал:
    .../subscribe POST подписка на пользователя
    .../subscribe DELETE удаление пользователя из подписок
    .../subscriptions GET просмотр на кого подписан пользователь
    .../newsfeed GET просмотр ленты новостей(подписок)

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, username=request.data["username"])
        # author = author.id
        if request.method == "POST":
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=[
            "GET",
        ],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=[
            "GET",
        ],
    )
    def newsfeed(self, request):
        user = request.user
        subscribed_users_subquery = (
            User.objects.filter(following__user=user).values("id")
        )
        queryset = Post.objects.filter(author_id__in=subscribed_users_subquery)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NewsFeedSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NewsFeedSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)
