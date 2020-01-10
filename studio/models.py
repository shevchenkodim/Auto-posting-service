from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime
User = get_user_model()


class SocialNetwork(models.Model):
    name = models.CharField("Назва", max_length=100)
    type = models.CharField("Тип", max_length=100)


class SocialNetworkFacebook(models.Model):
    name           = models.ForeignKey(SocialNetwork, null=False, blank=False, on_delete=models.CASCADE)
    login          = models.CharField(null=False, blank=False, max_length=100)
    password       = models.CharField(null=False, blank=False, max_length=100)
    connect_result = models.BooleanField(null=False, default=False)


class SocialNetworkTelegram(models.Model):
    name           = models.ForeignKey(SocialNetwork, null=False, blank=False, on_delete=models.CASCADE)
    name_channel   = models.CharField(null=False, blank=False, max_length=256)
    connect_result = models.BooleanField(null=False, default=False)


class Post(models.Model):
    user         = models.ForeignKey(
                                    User,
                                    verbose_name="Користувач",
                                    on_delete=models.CASCADE)
    sn_facebook      = models.ForeignKey(SocialNetworkFacebook, null=True, blank=True, on_delete=models.CASCADE)
    sn_telegram      = models.ForeignKey(SocialNetworkTelegram, null=True, blank=True, on_delete=models.CASCADE)
    title            = models.CharField("Заголовок", max_length=100)
    text             = models.TextField("Текст поста")
    images           = models.ImageField("Картинка", upload_to=settings.MEDIA_ROOT, blank=True, null=True)
    date_posting     = models.DateTimeField("Дата час коли викласти", blank=True, null=True)
    date_post_create = models.DateTimeField("Дата создания", auto_now_add=True, blank=True, null=True)
    connect_result = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.title
