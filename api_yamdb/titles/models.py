from django.db import models

from .validators import max_value_current_year


class Category(models.Model):
    name = models.TextField(
        verbose_name='Категория произведения',
        max_length=60,
        unique=True,
        db_index=True,
        help_text='Введите категорию произведения',
    )

    slug = models.SlugField(
        verbose_name='Категория',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.TextField(
        verbose_name='Название жанра',
        max_length=60,
        unique=True,
        db_index=True,
        help_text='Введите название жанра',
    )

    slug = models.SlugField(
        verbose_name='Жанр',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название произведения',
        max_length=200,
        db_index=True,
        help_text='Введите название произведения',
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Год релиза',
        null=True,
        blank=True,
        db_index=True,
        help_text='Год релиза',
        validators=(max_value_current_year,),
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
        help_text='Введите краткое описание произведения',
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=True,
        related_name='titles',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
