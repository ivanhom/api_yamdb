from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
# тут должны быть еще URL на пользователей, ревью, комментарии и систему авторизации (по моему связана с пользователями)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]