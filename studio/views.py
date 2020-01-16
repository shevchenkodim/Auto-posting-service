from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post, SocialNetwork, SocialNetworkTelegram, SocialNetworkFacebook, Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
import datetime
# Create your views here.

def studio(request):
    return render(request, "studio/main.html")

def saveprofile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('account_email','')
        file = request.FILES
        f = file.get('file')
        try:
            user = request.user
        except User.DoesNotExist:
            response_data = {'_code' : 1, '_status' : 'no' }
            return JsonResponse(response_data)
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            response_data = {'_code' : 1, '_status' : 'no' }
            return JsonResponse(response_data)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        if f != None:
            profile.image = f
        profile.save()
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)

def tasks(request):
    posts = Post.objects.filter(user = request.user)
    return render(request, "studio/tasks.html", {'posts':posts})


def taskcreate(request):
    telegrams = SocialNetworkTelegram.objects.filter(user=request.user)
    facebooks = SocialNetworkFacebook.objects.filter(user=request.user)
    return render(request, "studio/task_create.html", {'telegrams':telegrams, 'facebooks':facebooks})


def taskcreatenew(request):
    if request.method == 'POST':
        title        = request.POST.get('title','')
        text         = request.POST.get('text','')
        date_posting = request.POST.get('date_posting','')
        telegram     = SocialNetworkTelegram.objects.get(pk=request.POST.get('telegram',''))
        facebook     = SocialNetworkFacebook.objects.get(pk=request.POST.get('facebook',''))
        file         = request.FILES
        f            = file.get('file')
        try:
            task     = Post.objects.create(user=request.user, sn_facebook=facebook, sn_telegram=telegram, title=title, text=text, images=f, date_posting=date_posting, facebook_result=False, telegram_result=False)
            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            response_data = {'_code' : 1, '_status' : 'no' }
            print(e)

    return JsonResponse(response_data)


def taskdelete(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
    else:
        id = request.GET.get('id', '')
    try:
        task = Post.objects.get(id=id, user=request.user)
        task.delete()
        response_data = {'_code' : 0, '_status' : 'ok' }
        return JsonResponse(response_data)

    except Post.DoesNotExist:
        response_data = {'_code' : 1, '_status' : 'no' }
    return JsonResponse(response_data)


def statistics(request):
    return render(request, "studio/statistics.html")


def settings(request):
    telegram_acc = SocialNetworkTelegram.objects.filter(user=request.user)
    facebook_acc = SocialNetworkFacebook.objects.filter(user=request.user)
    return render(request, "studio/settings.html", {'telegram_acc':telegram_acc, 'facebook_acc':facebook_acc})


def createtelegram(request):
    if request.method == "POST":
        name_channel = request.POST.get('name_channel','')
        name         = SocialNetwork.objects.get(pk=2)
        telegram     = SocialNetworkTelegram.objects.create(user=request.user, name=name, name_channel=name_channel, connect_result=False)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def createfacebook(request):
    if request.method == "POST":
        login    = request.POST.get('login','')
        password = request.POST.get('password','')
        name     = SocialNetwork.objects.get(pk=1)
        telegram = SocialNetworkFacebook.objects.create(user=request.user, name=name, login=login, password=password, connect_result=False)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def deletetelegram(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
    else:
        id = request.GET.get('id', '')
    try:
        telegram = SocialNetworkTelegram.objects.get(id=id, user=request.user)
        telegram.delete()
        response_data = {'_code' : 0, '_status' : 'ok' }
        return JsonResponse(response_data)

    except SocialNetworkTelegram.DoesNotExist:
        response_data = {'_code' : 1, '_status' : 'no' }
    return JsonResponse(response_data)


def deletefacebook(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
    else:
        id = request.GET.get('id', '')
    try:
        facebook = SocialNetworkFacebook.objects.get(id=id, user=request.user)
        facebook.delete()
        response_data = {'_code' : 0, '_status' : 'ok' }
        return JsonResponse(response_data)

    except SocialNetworkFacebook.DoesNotExist:
        response_data = {'_code' : 1, '_status' : 'no' }
    return JsonResponse(response_data)
