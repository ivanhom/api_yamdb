from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

router = DefaultRouter()
router.register(r'v1/users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt'))
]
