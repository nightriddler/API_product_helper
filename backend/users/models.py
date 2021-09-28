from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчик'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='user and author restraint')]

    def __str__(self):
        return f'{self.user}->{self.author}'
