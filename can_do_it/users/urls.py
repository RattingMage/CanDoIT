from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import SkillViewSet

users_router = SimpleRouter()
users_router.register("users", UserViewSet, basename="users")

skill_router = SimpleRouter()
skill_router.register("skills", SkillViewSet, basename="skills")

urlpatterns = [
    path("", include(skill_router.urls)),
    path("", include(users_router.urls)),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]