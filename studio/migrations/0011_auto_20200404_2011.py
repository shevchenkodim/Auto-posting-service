# Generated by Django 2.1.14 on 2020-04-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0010_usermessages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessages',
            name='status_read',
            field=models.BooleanField(default=False, verbose_name='status_read'),
        ),
    ]
