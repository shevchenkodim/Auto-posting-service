# Generated by Django 2.1.14 on 2020-03-17 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studio', '0005_statistic'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач'),
            preserve_default=False,
        ),
    ]
