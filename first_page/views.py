from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from studio.models import Profile


class FirstPage(TemplateView):
    template_name = 'first_page.html'


class SignupPage(TemplateView):
    template_name = 'signup_page.html'


class LoginPage(TemplateView):
    template_name = 'login_page.html'


def register(request):
    if request.method == 'POST':
        form_regist = RegisterForm(request.POST)
        if form_regist.is_valid():
            user = form_regist.save()
            first_name = form_regist.cleaned_data.get('first_name')
            last_name = form_regist.cleaned_data.get('last_name')
            country = form_regist.cleaned_data.get('country')
            accept_license = form_regist.cleaned_data.get('accept_license')
            username = form_regist.cleaned_data.get('username')
            password = form_regist.cleaned_data.get('password')
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Your account is not registered!")


def authenticate_user(request):
    if request.method == 'POST':
        form_aut = AuthenticationForm(data=request.POST)
        if form_aut.is_valid():
            username = form_aut.cleaned_data.get('username')
            password = form_aut.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("You're account is disabled")


def user_logout(request):
    logout(request)
    return redirect('/')
