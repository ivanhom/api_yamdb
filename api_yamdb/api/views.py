from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.permissions import IsOwnerOrReadOnly, ReadOnly
from api.serializers import CreateUserSerialiser, UserSerializer
from users.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            return get_object_or_404(MyUser, username=self.request.user)
        return get_object_or_404(MyUser, username=username)

    def get_serializer_class(self):
        username = self.kwargs.get('username')
        if username == 'me':
            return CreateUserSerialiser
        return UserSerializer
