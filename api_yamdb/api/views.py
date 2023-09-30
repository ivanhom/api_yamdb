from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, mixins, permissions, serializers, status, viewsets
)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination
)
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.messages import INVALID_TOKEN_ERR
from api.mixins import CreateListViewSet, NoPutModelViewSet
from api.serializers import (
    CategorySerializer, CommentSerializer, CreateUserSerializer,
    GenreSerializer, GetTokenSerializer, ReviewSerializer,
    TitleSerializerRead, TitleSerializerWrite, UserSerializer
)
from api.permissions import (
    IsAdminOrReadOnly, IsAuthorOrJustReading, IsSuperUserOrAdmin
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class TitleViewSet(NoPutModelViewSet):
    """ViewSet модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
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
    permission_classes = (IsAuthorOrJustReading, IsAuthenticatedOrReadOnly)

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


class ReviewViewSet(NoPutModelViewSet):
    """ViewSet модели Review."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrJustReading)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        if Review.objects.filter(title_id=title_id, author=user).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.',
                status.HTTP_400_BAD_REQUEST
            )
        serializer.save(author=user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet модели User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)
    permission_classes = (IsSuperUserOrAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('get', 'patch',),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для регистрации нового пользователя."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, data = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Запрос кода подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserGetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для получения JWT токена."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            response = {'confirmation_code': INVALID_TOKEN_ERR}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': str(AccessToken.for_user(user))}
        return Response(data=response, status=status.HTTP_200_OK)
