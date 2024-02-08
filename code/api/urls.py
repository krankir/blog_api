from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import FollowViewSet, PostViewSet

app_name = "api"

router = DefaultRouter()


router.register("users", FollowViewSet)
router.register("posts", PostViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
