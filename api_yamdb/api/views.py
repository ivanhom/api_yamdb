from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from api.permissions import IsOwnerOrReadOnly, ReadOnly
from api.serializers import UserSerializer
from users.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()

    
