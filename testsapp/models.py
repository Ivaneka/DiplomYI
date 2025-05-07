from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание")
    assigned_to = models.ManyToManyField(User, verbose_name="Для пользователей")

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    text = models.TextField(verbose_name="Текст вопроса")

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.CharField(max_length=200, verbose_name="Ответ")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный")