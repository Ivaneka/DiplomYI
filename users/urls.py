from django.urls import path
from .views import CustomLoginView, RegisterView, custom_logout

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', custom_logout, name='logout'),
]