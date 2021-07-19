from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True
    )
    age = models.IntegerField(
        verbose_name='возраст',
        blank=True,
        null=True

    )
    is_deleted = models.BooleanField(default=False)
