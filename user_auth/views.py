from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView

from .forms import LoginForm

# Create your views here.
class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    @staticmethod
    def redirect_authenticated_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        else:
            return super().dispatch(request, *args, **kwargs)

