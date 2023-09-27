from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import MyUser


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,)
    slug = models.SlugField(
        max_length=50,
        unique=True,)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,)
    year = models.SmallIntegerField()
    genre = models.ManyToManyField(
        'Genre',
        related_name='genres',
        through='GenreTitle')
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        db_column='category',
        on_delete=models.SET_NULL,
        related_name='titles',)
    description = models.TextField(null=True,)

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    """Модель для отзывов."""
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='author')
    review = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review', null=True)
    text = models.TextField()
    image = models.ImageField(
        upload_to='review/', null=True, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='genre', blank=True, null=True
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)]
                )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    """Модель для комментов к отзывам."""
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comments')
    comment = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
