from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
User = get_user_model()


class SocialNetwork(models.Model):
    name = models.CharField("Назва", max_length=100)
    type = models.CharField("Тип", max_length=100)

    def __str__(self):
        return self.name

class SocialNetworkLiveJournal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='2')
    name = models.ForeignKey(SocialNetwork, null=False, blank=False, on_delete=models.CASCADE)
    login = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=100)
    connect_result = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.login


class SocialNetworkTelegram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='2')
    name = models.ForeignKey(SocialNetwork, null=False, blank=False, on_delete=models.CASCADE)
    name_channel = models.CharField(null=False, blank=False, max_length=256)
    connect_result = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name_channel


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name="Користувач", on_delete=models.CASCADE)
    sn_lj = models.ForeignKey(SocialNetworkLiveJournal, null=True, blank=True, on_delete=models.CASCADE)
    sn_telegram = models.ForeignKey(SocialNetworkTelegram, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст поста")
    images = models.ImageField("Картинка", upload_to=settings.MEDIA_ROOT, blank=True, null=True)
    date_posting = models.DateTimeField("Дата час коли викласти", blank=True, null=True)
    date_post_create = models.DateTimeField("Дата создания", auto_now_add=True, blank=True, null=True)
    facebook_result = models.BooleanField(null=False, default=False)
    telegram_result = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.title


class Statistic(models.Model):
    user = models.ForeignKey(User, verbose_name="Користувач", on_delete=models.CASCADE)
    date = models.DateField('Дата', default=timezone.now)
    post_create = models.IntegerField('Создано', default=0)

    def __str__(self):
        return str(self.date)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)

    def __str__(self):
        return self.user.username
