from rest_framework import serializers

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
