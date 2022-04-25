from django.db import models
from django.urls import reverse
# from django.core.signing import Signer
from django.utils import timezone
from datetime import timedelta


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
        db_table = 'account_user'
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
    key = models.CharField(max_length=256, unique= True)
    expires = models.DateTimeField()
    ip_addr = models.GenericIPAddressField(default='192.168.1.222')
    custom = SessionManager()
    objects = models.Manager()

    def __str__(self):
        return self.key
