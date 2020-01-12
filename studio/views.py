from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post, SocialNetwork, SocialNetworkTelegram, SocialNetworkFacebook
from django.http import JsonResponse
import datetime
# Create your views here.
def studio(request):
    return render(request, "studio/studio.html")

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
            task         = Post.objects.create(user=request.user, sn_facebook=facebook, sn_telegram=telegram, title=title, text=text, images=f, date_posting=date_posting, facebook_result=False, telegram_result=False)
            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            response_data = {'_code' : 1, '_status' : 'no' }
            print(e)

    return JsonResponse(response_data)


def statistics(request):
    return render(request, "studio/statistics.html")

def settings(request):
    telegram_acc = SocialNetworkTelegram.objects.filter(user=request.user)
    facebook_acc = SocialNetworkFacebook.objects.filter(user=request.user)
    return render(request, "studio/settings.html", {'telegram_acc':telegram_acc, 'facebook_acc':facebook_acc})


def settingscreatetelegram(request):
    if request.method == "POST":
        name_channel = request.POST.get('name_channel','')
        name         = SocialNetwork.objects.get(pk=2)
        telegram     = SocialNetworkTelegram.objects.create(user=request.user, name=name, name_channel=name_channel, connect_result=False)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def settingscreatefacebook(request):
    if request.method == "POST":
        login    = request.POST.get('login','')
        password = request.POST.get('password','')
        name     = SocialNetwork.objects.get(pk=1)
        telegram = SocialNetworkFacebook.objects.create(user=request.user, name=name, login=login, password=password, connect_result=False)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)
