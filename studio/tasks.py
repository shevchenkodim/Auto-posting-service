from Auto_posting_service.celery import app
from .models import Post, SocialNetworkLiveJournal
import xmlrpc.client as xmlrpclib
import time

@app.task
def live_journal_task(title, text, username, password, livejournal_id, post_id):
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

    return response


@app.task
def telegram_task(a, b):
    c = a + b
    return c
