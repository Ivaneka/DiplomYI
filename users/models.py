from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    # Дополнительные поля

# users/models.py
class CustomUser(AbstractUser):
    # Добавляем поля
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name="Аватар"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Отдел"
    )