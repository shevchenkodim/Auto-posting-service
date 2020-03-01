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
            users_list = User.objects.all()
            for users in users_list:
                if users.username == username:
                    response_data = {'_code' : 1, '_status' : 'ok', '_error':'Користувач з таким логіном вже є. Виберіть інший!' }
                    return JsonResponse(response_data)
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            print(e)
            response_data = {'_code' : 1, '_status' : 'no' }

        return JsonResponse(response_data)


def authenticate_user(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            login(request, user)
            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            print(e)
            response_data = {'_code' : 1, '_status' : 'ok', '_error':'Введено невірний логін або пароль!' }

        return JsonResponse(response_data)



def user_logout(request):
    logout(request)
    return redirect('/')
