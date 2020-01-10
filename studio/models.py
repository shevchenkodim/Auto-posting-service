from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(
            User,
            verbose_name="Автор",
            on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст статьи")
    images = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True, null=True)
    date_posting = models.DateTimeField("Дата", blank=True, null=True)
    moderation = models.IntegerField("Модерация", blank=True, null=True)

    def __str__(self):
        return self.title

class SocialNetwork(models.Model):
    name = models.CharField("Назва", max_length=100)
    type = models.CharField("Тип", max_length=100)    
