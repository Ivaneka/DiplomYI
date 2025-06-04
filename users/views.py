from django.contrib.auth.views import LoginView
from .forms import LoginForm

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'