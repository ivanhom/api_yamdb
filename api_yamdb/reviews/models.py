from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import MyUser


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
        ordering = ['-id']
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

    description = models.TextField(null=True,verbose_name='Описание',)
    
    class Meta:
        ordering = ['-id']
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
