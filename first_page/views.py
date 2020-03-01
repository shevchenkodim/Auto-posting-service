from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from studio.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import logout


class FirstPage(TemplateView):
    template_name = 'first_page.html'


class SignupPage(TemplateView):
    template_name = 'signup_page.html'


class LoginPage(TemplateView):
    template_name = 'login_page.html'


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.save()
            login(request, user)
            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            response_data = {'_code' : 1, '_status' : 'no' }

        return JsonResponse(response_data)


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
