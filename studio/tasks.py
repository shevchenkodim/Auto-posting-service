from Auto_posting_service.celery import app
from .models import Post, SocialNetworkLiveJournal, SocialNetworkTelegram
from django.core.mail import send_mail
import xmlrpc.client as xmlrpclib
import telebot
import time

BOT_TOKEN = "1087230616:AAGbBsbsr347z5MpX65XmjgZFsbBKxaYdRE"
bot = telebot.TeleBot(BOT_TOKEN)


@app.task(bind=True)
def send_verify_email_task(self, email, uuid):
    try:
        send_mail(
            'Verify your Auto posting account',
            'Follow this link to verify your account: '
            'http://localhost:8000/studio/verify/'+ str(uuid),
            'djangos99@gmail.com',
            [email],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60, max_retries=3)
    return True


@app.task(bind=True)
def live_journal_task(self, title, text, username, password, livejournal_id, post_id):
    try:
        ljsrv = xmlrpclib.ServerProxy(r"http://www.livejournal.com/interface/xmlrpc")
        curtime = time.localtime()

        data = {'ver':1,
         'subject': title,
         'year': curtime[0],
         'mon': curtime[1],
         'day': curtime[2],
         'hour': curtime[3],
         'min': curtime[4],
         'security': 'private',
         'event': text,
         'username': username,
         'password': password,
         }
        response = ljsrv.LJ.XMLRPC.postevent(data)
        Post.objects.filter(id=post_id).update(live_journal_result=True)
        SocialNetworkLiveJournal.objects.filter(id=livejournal_id).update(connect_result=True)

    except Exception as exc:
        Post.objects.filter(id=post_id).update(live_journal_result=False)
        SocialNetworkLiveJournal.objects.filter(id=livejournal_id).update(connect_result=False)
        raise self.retry(exc=exc, countdown=60, max_retries=3)
    return True


@app.task(bind=True)
def telegram_task(self, text, channel_name, image_path, telegram_id, post_id):
    try:
        administrator = False
        users = bot.get_chat_administrators(channel_name)
        for user in users:
            if user.user.username == 'auto_posting_adminbot':
                if user.status == 'administrator':
                    administrator = True
                    SocialNetworkTelegram.objects.filter(id=telegram_id).update(connect_result=True)
                else:
                    SocialNetworkTelegram.objects.filter(id=telegram_id).update(connect_result=False)
                    administrator = False

        if administrator == True:
            if image_path != '':
                PHOTO = open(image_path, 'rb')
                bot.send_photo(channel_name, PHOTO, text)
            else:
                bot.send_message(channel_name, text)
            Post.objects.filter(id=post_id).update(telegram_result=True)

    except Exception as exc:
        Post.objects.filter(id=post_id).update(telegram_result=False)
        raise self.retry(exc=exc, countdown=60, max_retries=3)

    return True
