from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comments, Review
from .permissions import IsAuthorOrJustReading
from .serializers import (CommentsSerializer, ReviewSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrJustReading, )
    pagination_class = LimitOffsetPagination

    def get_related_post(self):
        return get_object_or_404(Comments, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_related_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_related_post()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Review.objects.all()
    pagination_class = LimitOffsetPagination

    def get_related_post(self):
        return get_object_or_404(Review, pk=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_related_post()
        )
