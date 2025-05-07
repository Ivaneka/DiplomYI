from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    # Дополнительные поля

# В settings.py добавляем:
AUTH_USER_MODEL = 'users.CustomUser'