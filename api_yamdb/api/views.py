from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title

from api.filters import TitleFilter
from api.mixins import CreateListViewSet, NoPutModelViewSet
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializerRead, TitleSerializerWrite)

from .permissions import IsAdminOrReadOnly, IsAuthorOrJustReading


class TitleViewSet(NoPutModelViewSet):
    """ViewSet модели Title."""

    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite


class CategoryViewSet(CreateListViewSet):
    """ViewSet модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    """ViewSet модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CommentViewSet(NoPutModelViewSet):
    """ViewSet модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrJustReading)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']
    pagination_class = PageNumberPagination

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
