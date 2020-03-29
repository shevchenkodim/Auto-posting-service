from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .models import Post, SocialNetwork, SocialNetworkTelegram, SocialNetworkLiveJournal, Profile, Statistic
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .tasks import live_journal_task, telegram_task
from Auto_posting_service.celery import app
from django.conf import settings
from django.core.mail import send_mail
import dateutil.parser
import datetime
import pytz
# Create your views here.

class Studio(TemplateView):
    template_name = "studio/main.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        return render(request, self.template_name)


def saveprofile(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
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
        t = my_task.delay(3, 2)
        print(t)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


class SocialNetworkPage(TemplateView):
    template_name = "studio/social_network.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        telegram_acc = SocialNetworkTelegram.objects.filter(user=request.user)
        return render(request, self.template_name, {'telegram_acc':telegram_acc})

class SocialNetworkLiveJournalPage(TemplateView):
    template_name = "studio/social_network_livejournal.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        livejournal_acc = SocialNetworkLiveJournal.objects.filter(user=request.user)
        return render(request, self.template_name, {'livejournal_acc':livejournal_acc})


class Help(TemplateView):
    template_name = "studio/help.html"


class Tasks(TemplateView):
    template_name = "studio/tasks.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        posts = Post.objects.filter(user = request.user)
        return render(request, self.template_name, {'posts':posts})


class Taskscreate(TemplateView):
    template_name = "studio/task_create.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        telegrams = SocialNetworkTelegram.objects.filter(user=request.user)
        livejournal = SocialNetworkLiveJournal.objects.filter(user=request.user)
        date_posting = datetime.datetime.now()
        return render(request, self.template_name, {'telegrams':telegrams, 'livejournals':livejournal, 'date_posting':date_posting})


class Taskupdate(TemplateView):
    template_name = "studio/task_update.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        post = Post.objects.get(pk=self.kwargs['pk'])
        telegrams = SocialNetworkTelegram.objects.filter(user=request.user)
        livejournal = SocialNetworkLiveJournal.objects.filter(user=request.user)
        return render(request, self.template_name, {'telegrams':telegrams, 'livejournals':livejournal, 'post':post})


def taskupdatesave(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == 'POST':
        title = request.POST.get('title','')
        text = request.POST.get('text','')
        date_posting = request.POST.get('date_posting','')

        my_date = dateutil.parser.parse(date_posting)
        indy = pytz.timezone("Europe/Kiev")
        my_date = indy.localize(my_date)

        if request.POST.get('telegram','') == '':
            telegram = None
        else:
            telegram = SocialNetworkTelegram.objects.get(pk=request.POST.get('telegram',''))
        if request.POST.get('livejournal','') == '':
            livejournal = None
        else:
            livejournal = SocialNetworkLiveJournal.objects.get(pk=request.POST.get('livejournal',''))
        file = request.FILES
        f = file.get('file')
        try:
            task = Post.objects.get(user=request.user, pk=pk)
            task.sn_lj=livejournal
            task.sn_telegram=telegram
            task.title=title
            task.text=text
            if f != None:
                task.images=f
            task.date_posting=my_date
            task.live_journal_result=False
            task.telegram_result=False
            task.save()

            try:
                app.control.revoke(task.telegram_task_id)
            except Exception as e:
                print(e)
            try:
                app.control.revoke(task.live_journal_task_id)
            except Exception as e:
                print(e)

            if livejournal != None:
                try:
                    post_text = task.text
                    if task.images != '':
                        image_str = '<div style="text-align:center"><img src="http://127.0.0.1:8000'+ task.images.url +'" width="500" height="auto"/></div><br>'
                        new_text = image_str + task.text
                        post_text = new_text
                    result = live_journal_task.apply_async((task.title, post_text, livejournal.login, livejournal.password, livejournal.id, task.id), eta=my_date)
                    task.live_journal_task_id = result.id
                    task.save()
                except Exception as e:
                    print(e)

            if telegram != None:
                try:
                    image_path = str(task.images)
                    result_telegram = telegram_task.apply_async((task.text, telegram.name_channel, image_path, telegram.id,  task.id), eta=my_date)
                    task.telegram_task_id = result_telegram.id
                    task.save()
                except Exception as e:
                    print(e)

            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def taskcreatenew(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == 'POST':
        title = request.POST.get('title','')
        text = request.POST.get('text','')
        date_posting = request.POST.get('date_posting','')

        my_date = dateutil.parser.parse(date_posting)
        indy = pytz.timezone("Europe/Kiev")
        my_date = indy.localize(my_date)

        if request.POST.get('telegram','') == '':
            telegram = None
        else:
            telegram = SocialNetworkTelegram.objects.get(pk=request.POST.get('telegram',''))

        if request.POST.get('livejournal','') == '':
            livejournal = None
        else:
            livejournal = SocialNetworkLiveJournal.objects.get(pk=request.POST.get('livejournal',''))

        file = request.FILES
        f = file.get('file')
        try:
            task = Post.objects.create(user=request.user, sn_lj=livejournal, sn_telegram=telegram, title=title, text=text, images=f, date_posting=my_date, live_journal_result=False, telegram_result=False)
            try:
                staistic = Statistic.objects.get(user=request.user, date=timezone.now())
            except Statistic.DoesNotExist:
                staistic = None
            if staistic == None:
                obj = Statistic.objects.create(user=request.user, date=timezone.now())
                obj.post_create += 1
                obj.save(update_fields=['post_create'])
            else:
                staistic.post_create += 1
                staistic.save(update_fields=['post_create'])

            if livejournal != None:
                post_text = task.text
                if task.images != None:
                    image_str = '<div style="text-align:center"><img src="http://127.0.0.1:8000'+ task.images.url +'" width="500" height="auto"/></div><br>'
                    new_text = image_str + task.text
                    post_text = new_text
                result = live_journal_task.apply_async((task.title, post_text, livejournal.login, livejournal.password, livejournal.id, task.id), eta=my_date)
                task.live_journal_task_id = result.id
                task.save()

            if telegram != None:
                image_path = str(task.images)
                result_telegram = telegram_task.apply_async((task.text, telegram.name_channel, image_path, telegram.id,  task.id), eta=my_date)
                task.telegram_task_id = result_telegram.id
                task.save()

            response_data = {'_code' : 0, '_status' : 'ok' }
        except Exception as e:
            response_data = {'_code' : 1, '_status' : 'no' }
            print(e)

    return JsonResponse(response_data)


def taskdelete(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
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


class Statistics(TemplateView):
    template_name = "studio/statistics.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        statistic_list = Statistic.objects.filter(user=self.request.user).order_by('date')

        return render(request, self.template_name, {'statistic_list':statistic_list})


class Settings(TemplateView):
    template_name = "studio/settings.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        return render(request, self.template_name)


def createtelegram(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == "POST":
        name_channel = '@' + request.POST.get('name_channel','')
        name = SocialNetwork.objects.get(pk=2)
        telegram = SocialNetworkTelegram.objects.create(user=request.user, name=name, name_channel=name_channel, connect_result=False)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def createlivejournal(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == "POST":
        login = request.POST.get('login','')
        password = request.POST.get('password','')
        name = SocialNetwork.objects.get(pk=1)
        livejournal = SocialNetworkLiveJournal.objects.create(user=request.user, name=name, login=login, password=password, connect_result=False)
        response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def deletetelegram(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
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


def deletelivejournal(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == 'POST':
        id = request.POST.get('id', '')
    else:
        id = request.GET.get('id', '')
    try:
        livejournal = SocialNetworkLiveJournal.objects.get(id=id, user=request.user)
        livejournal.delete()
        response_data = {'_code' : 0, '_status' : 'ok' }
        return JsonResponse(response_data)

    except SocialNetworkLiveJournal.DoesNotExist:
        response_data = {'_code' : 1, '_status' : 'no' }
    return JsonResponse(response_data)


def verify(request, uuid):
    try:
        user = Profile.objects.get(verification_uuid=uuid, is_verified=False)
    except Profile.DoesNotExist:
        raise Http404("User does not exist or is already verified")
    user.is_verified = True
    user.save()

    return redirect(reverse('first_page:login_page'))


def send_verify_email(email, uuid):
        send_mail(
            'Verify your Auto posting account',
            'Follow this link to verify your account: '
            'http://localhost:8000/studio/verify/'+ str(uuid),
            'djangos99@gmail.com',
            [email],
            fail_silently=False,
        )


def permission_denied(request):
    data = {}
    return render(request, '403.html', data, status=403)
