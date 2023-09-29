from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""
    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, value):
        # if MyUser.objects.filter(username=value.get('username')):
        #     raise serializers.ValidationError(
        #         'Такой пользователь уже существует'
        #     )
        # if MyUser.objects.filter(email=value.get('email')):
        #     raise serializers.ValidationError(
        #         'Пользователь с такой почтой уже существует'
        #     )
        if value.get('username') == 'me':
            raise serializers.ValidationError(
                'Запрещено и спользовать имя me'
            )
        return value


class CreateUserSerialiser(UserSerializer):
    """Сериалайзер для создания объекта модели User."""     # Хрень
    class Meta:
        model = MyUser
        fields = ('email', 'username')


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
