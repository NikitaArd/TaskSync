from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)


class TaskManager(models.Manager):

    def get_by_sequence(self, tasks_seq, columns):
        tasks = super().get_queryset().filter(column__in=columns)
        tasks_list = []
        for column in columns:
            for seq in tasks_seq.get(column=column).tasks:
                tasks_list.append(tasks.get(id=seq))

        return tasks_list
