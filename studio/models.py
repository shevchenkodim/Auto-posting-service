from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
import uuid
User = get_user_model()


class SocialNetwork(models.Model):
    """Social Network"""
    name = models.CharField("Name", max_length=100)
    type = models.CharField("Type", max_length=100)

    def __str__(self):
        return self.name

class SocialNetworkLiveJournal(models.Model):
    """Social Network for LiveJournal"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='2')
    name = models.ForeignKey(SocialNetwork, null=False, blank=False, on_delete=models.CASCADE)
    login = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=100)
    connect_result = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.login


class SocialNetworkTelegram(models.Model):
    """Social Network for Telegram"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='2')
    name = models.ForeignKey(SocialNetwork, null=False, blank=False, on_delete=models.CASCADE)
    name_channel = models.CharField(null=False, blank=False, max_length=256)
    connect_result = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name_channel


class Post(models.Model):
    """Tasks (post in social network)"""
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    sn_lj = models.ForeignKey(SocialNetworkLiveJournal, null=True, blank=True, on_delete=models.CASCADE)
    sn_telegram = models.ForeignKey(SocialNetworkTelegram, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=100)
    text = models.TextField("Text")
    images = models.ImageField("Image", upload_to=settings.MEDIA_ROOT, blank=True, null=True)
    date_posting = models.DateTimeField("Date when posting", blank=True, null=True)
    date_post_create = models.DateTimeField("Date create", auto_now_add=True, blank=True, null=True)
    live_journal_result = models.BooleanField(null=False, default=False)
    telegram_result = models.BooleanField(null=False, default=False)
    telegram_task_id = models.UUIDField(default=uuid.uuid4)
    live_journal_task_id = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.title


class Statistic(models.Model):
    """Statistic for user"""
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    date = models.DateField('Date', default=timezone.now)
    post_create = models.IntegerField('Created', default=0)

    def __str__(self):
        return str(self.date)


class Profile(models.Model):
    """Profile user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    def __str__(self):
        return self.user.username


class UserMessages(models.Model):
    """Messages for user"""
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    title =  models.CharField("Name", max_length=100)
    short_text = models.TextField("Text", max_length=256)
    text = models.TextField("Text")
    photo = models.ImageField("Image", upload_to=settings.MEDIA_ROOT)
    date = models.DateTimeField("Date create", auto_now_add=True)
    status_read = models.BooleanField("status read", default=False)

    def __str__(self):
        return f'{self.user} - {self.title}'
