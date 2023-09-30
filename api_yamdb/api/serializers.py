from django.contrib.auth import get_user_model
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
        if data.get('username') == 'me':
            raise serializers.ValidationError(USER_CREATE_ME_ERR)
        return data


class CreateUserSerializer(serializers.Serializer):
    """Сериалайзер для регистрации нового пользователя."""
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150
    )

    def validate(self, data):
        email_in_db = User.objects.filter(email=data.get('email'))
        username_in_db = User.objects.filter(username=data.get('username'))

        if data.get('username') == 'me':
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
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerWrite(serializers.ModelSerializer):
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
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
