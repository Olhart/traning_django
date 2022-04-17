from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db.models.aggregates import Sum
# from django.core.signing import Signer
from django.utils import timezone
from datetime import timedelta

class ForumManager(models.Manager):
    def get_messages_with_rating(self, pk):
        msgs = self.filter(pk=pk).values('message', 'message__text', "message__author__username",'message__create_date', 'message__is_head', 'id').annotate(rating=Sum("message__messagerating__mark"))
        return msgs

class User(models.Model):
    username = models.CharField("Логин", max_length=32, unique=True)
    first_name = models.CharField("Имя", max_length=32, blank=True) 
    last_name = models.CharField("Фамилия", max_length=32, blank=True)
    password = models.CharField(max_length=24)
    email_address = models.EmailField("Email", unique=True)
    create_date = models.DateField("Дата создания", auto_now_add=True)
    photo = models.ImageField(upload_to="photo_users/%Y/%m/%d/", verbose_name="Фото", blank=True)
    last_active_date = models.DateTimeField("Заходил последний раз")
    ban = models.BooleanField("Бан", default=False)

    def get_absolute_url(self):
            return reverse('forum:user', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username',]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class SessionManager(models.Manager):
    def do_login(self, login, password):
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return None
        if user.password != password:
            return None
        self = Session()
        value = str(login) + str(password)
        self.key = value
        self.user = user
        self.expires = timezone.now() + timedelta(days=1)
        self.save()
        try:
            old_session=Session.objects.get(user=user, expires__lt=timezone.now())
        except self.DoesNotExist:
            return self
        old_session.delete()
        return self

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=256)
    expires = models.DateTimeField()
    ip_addr = models.GenericIPAddressField(default='192.168.1.222')
    custom = SessionManager()
    objects = models.Manager()

    def __str__(self):
        return self.key

class Category(models.Model):
    name = models.CharField(max_length=156)

    def __str__(self):
        return self.name

class Forum(models.Model):
    title = models.CharField("Название", max_length=256)
    url = models.SlugField('Слаг', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="deleted", verbose_name='Создатель')
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    custom = ForumManager()
    objects = models.Manager()

    def get_absolute_url(self):
            return reverse('forum:topic', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = "Форум"
        verbose_name_plural = "Форумы"

class Message(models.Model):
    text = models.TextField("Текст")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name="Форум")
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="deleted", verbose_name='Автор')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    create_date = models.DateTimeField("Время создания", auto_now_add=True)
    refer = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    last_edit_date = models.DateTimeField("Время последнего редактирования", auto_now=True)
    is_head = models.BooleanField("Первое сообщение", default=False)

    def __str__(self):
        return self.text

class MessageRating(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0, validators=[MaxValueValidator(1),MinValueValidator(-1)])

    class Meta:
        unique_together = [['message', 'author']]