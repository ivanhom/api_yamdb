from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'


class UserRole(models.TextChoices):
    admin = ADMIN
    moderator = MODERATOR
    user = USER


class MyUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150,
        validators=(RegexValidator(
            regex=settings.USERNAME_REGEX,
            message='Недопустимый символ в имени пользователя'
        ),),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Допустимы буквы, цифры и символы: @/./+/-/_.'
        )
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=UserRole.choices,
        max_length=20,
        blank=False,
        default=USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:20]

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
