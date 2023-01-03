from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title

User = get_user_model()

DISPLAYED_LETTERS = 15


class Review(models.Model):

    MIN_SCORE_VALUE = 1
    MAX_SCORE_VALUE = 10

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Произведение, к которой будет относиться ревью',
    )

    text = models.TextField(
        verbose_name='Текст отзыва',
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        validators=(
            MinValueValidator(
                MIN_SCORE_VALUE,
                f'Минимальное значение оценки: {MIN_SCORE_VALUE}'
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                f'Максимальное значение оценки: {MAX_SCORE_VALUE}'
            ),
        ),
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review',
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:DISPLAYED_LETTERS]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Отзыв, к которой будет относиться комментарий',
    )

    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст нового комментария',
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:DISPLAYED_LETTERS]
