# Generated by Django 2.1.14 on 2020-03-22 10:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0007_auto_20200322_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='live_journal_task_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='post',
            name='telegram_task_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
