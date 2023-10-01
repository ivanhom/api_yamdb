from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.messages import (
    USER_CREATE_EXIST_EMAIL_ERR, USER_CREATE_EXIST_NAME_ERR,
    USER_CREATE_ME_ERR
)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == settings.USER_INFO_URL_PATH:
            raise serializers.ValidationError(USER_CREATE_ME_ERR)
        return data


class CreateUserSerializer(serializers.Serializer):
    """Сериалайзер для регистрации нового пользователя."""
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=settings.USERNAME_REGEX,
        required=True,
        max_length=150
    )

    def validate(self, data):
        email_in_db = User.objects.filter(email=data.get('email'))
        username_in_db = User.objects.filter(username=data.get('username'))

        if data.get('username') == settings.USER_INFO_URL_PATH:
            raise serializers.ValidationError(USER_CREATE_ME_ERR)
        if email_in_db:
            if username_in_db:
                return data
            raise serializers.ValidationError(USER_CREATE_EXIST_EMAIL_ERR)
        else:
            if username_in_db:
                raise serializers.ValidationError(USER_CREATE_EXIST_NAME_ERR)
            return data


class GetTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения JWT токена."""
    username = serializers.RegexField(
        regex=settings.USERNAME_REGEX,
        required=True,
        max_length=150
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для Категорий."""
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для Жанров."""
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериалайзер для Произведений(их названий)."""
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)
    rating = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerWrite(serializers.ModelSerializer):
    """Сериалайзер для Произведений(их названий)."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError('Может существовать '
                                              'только один отзыв.')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для Комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
