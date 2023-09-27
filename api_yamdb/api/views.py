from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from api.mixins import CreateListViewSet
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
    CommentSerializer,
    ReviewSerializer
)
from reviews.models import Category, Genre, Title, Review, Comment
from .permissions import IsAuthorOrJustReading


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet модели Title."""

    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerRead
        return TitleSerializerWrite


class CategoryViewSet(CreateListViewSet):
    """ViewSet модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    """ViewSet модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrJustReading)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']
    pagination_class = LimitOffsetPagination

    def get_related_post(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_related_post().comments.all()

    def perform_create(self, serializer):
        related_post = self.get_related_post()
        serializer.save(
            author=self.request.user,
            comment=related_post
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrJustReading)
    queryset = Review.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
