from django.contrib import admin
from .models import (
    Test,
    Question,
    Answer,
    TestResult,
    Material,
    TestCategory,
    UserProfile
)


# 1. Инлайн для ответов
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    min_num = 1


# 2. Админка для вопросов
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'test')
    list_filter = ('test',)


# 3. Админка для категорий тестов
@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# 4. Админка для тестов
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description_short')
    list_filter = ('category',)
    search_fields = ('title', 'category__name')

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    description_short.short_description = 'Описание'


# 5. Админка для материалов
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_test', 'created_at')
    list_filter = ('related_test',)


# 6. Админка для профилей пользователей
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position')
    search_fields = ('user__username', 'department')


# 7. Регистрируем оставшиеся модели
admin.site.register(TestResult)
admin.site.register(Answer)