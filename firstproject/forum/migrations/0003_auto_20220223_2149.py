# Generated by Django 3.2.12 on 2022-02-23 17:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20220222_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_head',
            field=models.BooleanField(default=False, verbose_name='Первое сообщение'),
        ),
        migrations.AlterField(
            model_name='messagerating',
            name='mark',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(-1)]),
        ),
        migrations.DeleteModel(
            name='ForumRating',
        ),
    ]
