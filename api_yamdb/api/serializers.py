from rest_framework import serializers

from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""
    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
