# Generated by Django 2.1.14 on 2020-03-17 21:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0004_auto_20200310_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('post_create', models.IntegerField(default=0, verbose_name='Создано')),
            ],
        ),
    ]
