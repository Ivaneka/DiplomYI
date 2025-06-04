from django.contrib import admin
from .models import Material
from .models import Test, Question, Answer, TestResult, Material  # Добавлен импорт Material

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 1

@admin.register(Question)  # Используем декоратор для регистрации
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

@admin.register(Material)  # Используем декоратор для регистрации
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_test', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('related_test',)

# Регистрируем остальные модели
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Answer)  # Добавил регистрацию модели Answer