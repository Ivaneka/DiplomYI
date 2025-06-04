from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="ID")
    title = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание")
    assigned_to = models.ManyToManyField(User, verbose_name="Для пользователей")

    def __str__(self):
        return f"{self.title} (ID: {self.id})"


class Material(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание")
    related_test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="Связанный тест")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="ID")
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name="Тест")
    text = models.TextField(verbose_name="Текст вопроса")

    def __str__(self):
        return f"Вопрос ID {self.id} из теста '{self.test.title}'"


class Answer(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="ID")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.CharField(max_length=200, verbose_name="Ответ")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный")

    def __str__(self):
        return f"Ответ ID {self.id} ({'✓' if self.is_correct else '✗'})"


class TestResult(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField(verbose_name="Баллы")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")

    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

    def __str__(self):
        return (
            f"Результат ID {self.id} | "
            f"Пользователь: {self.user.username} | "
            f"Тест: {self.test.title}"
        )