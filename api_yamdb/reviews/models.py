from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
        unique=True,)
    slug = models.SlugField(
        verbose_name='Slug произведения',
        max_length=50,
        unique=True,)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,)

    year = models.SmallIntegerField(
        verbose_name='Год выпуска',)

    genre = models.ManyToManyField(
        'Genre',
        related_name='genres',
        through='GenreTitle',
        verbose_name='Жанр',)

    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        db_column='category',
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',)

    description = models.TextField(null=True, verbose_name='Описание',)
    # rating = models.FloatField(null=True, blank=True) возможно надо добавить

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категории'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь жанр-произведение'
        verbose_name_plural = 'Связь жанр-произведение'

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    """Модель для отзывов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title', null=True)
    text = models.TextField()
    image = models.ImageField(
        upload_to='review/', null=True, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='genre', blank=True, null=True
    )
    score = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(10)
        )
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """Модель для комментов к отзывам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    comment = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.name
