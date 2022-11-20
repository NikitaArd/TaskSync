from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.conf import settings

import uuid

from .managers import CustomUserManager


class Avatar(models.Model):
   source_image = models.ImageField(blank=False, verbose_name='Obraz żródłowy')
   search_slug = models.CharField(unique=True, max_length=20, blank=False, null=False, verbose_name='Pole wuszikwania')
    
   def __str__(self) -> str:
       return self.search_slug


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    username = models.CharField(max_length=80, blank=True, verbose_name='Username użytkownika', default='Username')
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name='email użytkownika')

    first_name = models.CharField(max_length=40, blank=False, verbose_name='Imię użytkownika')
    second_name = models.CharField(max_length=40, blank=False, verbose_name='Nazwisko użytkownika')

    registration_datetime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Data rejestracji')
    user_avatar = models.ForeignKey(Avatar, on_delete=models.PROTECT, default=Avatar.objects.get(search_slug=settings.DEFAULT_AVATAR).id, verbose_name='Avatar użytkownika')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return '{} | {}'.format(self.username, self.email)

class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return name

    def check_user_is_member(self, user_uuid):

        if self.members.members.filter(uuid=user_uuid):
            return True

        return False

# All Signals

# User signals
def pre_save_user_dispatcher(sender, **kwargs):
    kwargs['instance'].username = '{} {}'.format(kwargs['instance'].first_name, kwargs['instance'].second_name)

pre_save.connect(pre_save_user_dispatcher, sender=CustomUser)
