from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('testsapp:cabinet')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Добавлен импорт login
        return redirect(self.success_url)

def custom_logout(request):
    logout(request)
    return redirect('users:login')