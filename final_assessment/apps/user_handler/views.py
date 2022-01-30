from django.views.generic.base import View
from django.views.generic.edit import FormView
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import Login, Registration

# Create your views here.


class Registration(FormView):
    form_class = Registration
    template_name = 'user_handler/registration.html'

    def form_valid(self, form):
        return render(self.request, 'user_handler/registration.html', self.get_custom_context_data(form))
    
    def get_custom_context_data(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            confirm_password = form.cleaned_data.get("confirm_password")
            password = form.cleaned_data.get("password")
        if CustomUser.objects.filter(email=email).exists():
            context['error'] = 'Podany użytkownik już istnieje'
            return context
        if password != confirm_password:
            context['error'] = 'Hasła muszą być takie same'
            return context
        new_user = CustomUser(email=email, hash=password)
        new_user.save()
        context['success'] = 'Konto zostało założone'
        return context

class Login(FormView):
    form_class = Login
    template_name = 'user_handler/login.html'

    def form_valid(self, form):
        password_correct = False

        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')

        user_exists = CustomUser.objects.filter(email=user_email).exists()

        if user_exists:
            user = CustomUser.objects.filter(email=user_email).first()
            password_correct = user.hash == user_password

        if user_exists and password_correct:
            login(self.request, user)
            return redirect('/')

        return render(self.request, 'user_handler/login.html', self.get_custom_context_data(user_exists, password_correct))

    def get_custom_context_data(self, user_exists, password_correct, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not user_exists:
            context['error'] = 'Podany użytkownik nie istnieje'
            return context

        if not password_correct:
            context['error'] = 'Błędne hasło'
        return context

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')
