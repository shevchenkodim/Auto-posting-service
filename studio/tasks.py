from Auto_posting_service.celery import app
from .models import Post, SocialNetworkLiveJournal, SocialNetworkTelegram
import xmlrpc.client as xmlrpclib
import telebot
import time

BOT_TOKEN = "1087230616:AAGbBsbsr347z5MpX65XmjgZFsbBKxaYdRE"
bot = telebot.TeleBot(BOT_TOKEN)

@app.task
def live_journal_task(title, text, username, password, livejournal_id, post_id):
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

        post = Post.objects.get(id=post_id)
        post.live_journal_result = True
        post.save()
        livejournal = SocialNetworkLiveJournal.objects.get(id=livejournal_id)
        livejournal.connect_result = True
        livejournal.save()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60, max_retries=3)
    return response


@app.task
def telegram_task(text, channel_name, image_path, telegram_id, post_id):
    try:
        administrator = False
        users = bot.get_chat_administrators(channel_name)
        for user in users:
            if user.user.username == 'auto_posting_adminbot':
                if user.status == 'administrator':
                    administrator = True
                    telegram = SocialNetworkTelegram.objects.get(id=telegram_id)
                    telegram.connect_result = True
                    telegram.save()
                else:
                    administrator = False

        post = Post.objects.get(id=post_id)
        if administrator == True:
            if image_path != '':
                PHOTO = open(image_path, 'rb')
                bot.send_photo(channel_name, PHOTO, text)
            else:
                bot.send_message(channel_name, text)

        post.telegram_result = True
        post.save()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60, max_retries=3)

    return True
