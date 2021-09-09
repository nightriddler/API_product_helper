from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# class User(AbstractUser):
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [
#         'username',
#         'first_name',
#         'last_name',
#         ]

#     email = models.EmailField(
#         _('email address'),
#         help_text='Введите почту',
#         unique=True
#     )
    
#     first_name = models.CharField(_('first name'), max_length=150, blank=False)
#     last_name = models.CharField(_('last name'), max_length=150, blank=False)

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
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='user and author restraint')]

    def __str__(self):
        return f'{self.user}->{self.author}'