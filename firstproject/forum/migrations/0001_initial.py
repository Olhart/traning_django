# Generated by Django 3.2.12 on 2022-02-14 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(blank=True, max_length=32, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=32, verbose_name='Фамилия')),
                ('password', models.CharField(max_length=24)),
                ('email_address', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('last_active_date', models.DateTimeField(auto_now=True, verbose_name='Заходил последний раз')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('ban', models.BooleanField(default=False, verbose_name='Бан')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('last_change_date', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('author', models.ForeignKey(default='deleted', on_delete=django.db.models.deletion.SET_DEFAULT, to='forum.user', verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Форум',
                'verbose_name_plural': 'Форумы',
                'ordering': ['title'],
            },
        ),
    ]