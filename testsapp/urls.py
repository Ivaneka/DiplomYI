from django.urls import path
from . import views

app_name = 'testsapp'  # Объявление пространства имен

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('cabinet/', views.personal_cabinet, name='cabinet'),
    path('register/', views.register, name='register'),
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
]