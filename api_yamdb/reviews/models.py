from django.db import models

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