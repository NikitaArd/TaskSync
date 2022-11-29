from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.db.models.signals import (
        pre_save,
        post_save,
        pre_delete,
        )

import uuid

from .managers import (
        CustomUserManager,
        TaskManager,
        )


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
    max_members = models.IntegerField(default=2)

    def __str__(self) -> str:
        return '{} | {}'.format(self.name, self.owner.username)

    def check_user_is_member(self, user_uuid):

        if self.members.members.filter(uuid=user_uuid):
            return True

        return False

    def change_project_settings(self, new_project_name:str, new_max_members:int) -> bool:

        if not self.name == new_project_name or not self.max_members == new_max_members:

            if new_max_members < self.memberpool.members.count():
                
                return False

            self.name = new_project_name
            self.max_members = new_max_members
            self.save()

        return True



class MemberPool(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(CustomUser)

    def __str__(self) -> str:
        return '{} Pool'.format(self.project.name)

    def user_delete(self, user_object):
        
        if user_object == self.project.owner:
            return False

        try:
            self.members.remove(user_object)
            self.save()
            return True
        except Exception as e:
            return False

    def user_add(self, user_object):
        
        if self.members.count() >= self.project.max_members:
            return False

        try:
            self.members.add(user_object)
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
        

class Column(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    name = models.CharField(max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return '{} | {}'.format(self.name, self.project.name)

class Task(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    content = models.CharField(max_length=80)
    done_status = models.BooleanField(default=False)
    column = models.ForeignKey(Column, blank=False, on_delete=models.CASCADE)

    objects = TaskManager()

    def __str__(self) -> str:
        return '{} | {}'.format(self.content, self.column.name)

    def toggle_status(self):
        self.done_status = not self.done_status
        self.save()
    
    def change_content(self, new_content):
        if len(new_content) <= 80:
            self.content = new_content
            self.save()
            
            return True
        return False

class TasksSeq(models.Model):
    tasks = ArrayField(models.CharField(max_length=20), size=16, blank=True)
    column = models.OneToOneField(Column, on_delete=models.CASCADE, blank=True, default=None)

    def __str__(self) -> str:
        return '{} | {}'.format(self.column.name, self.column.project.name) 

    def add_task_to_seq(self, id):
        try:
            self.tasks.append(id)
            self.save()

            return True
        except Exception:
            return False

    def delete_task_from_seq(self, id):
        try:
            self.remove(str(id))
            self.save()

            return True
        except Exception:

            return False

    def shift_task(self, prev_task_uuid, task_uuid, user_uuid): # Function to change task in sequence (ex. [3, 2, 1] -> [3, 1, 2])

        try:
            self.column.project.members.members.get(uuid=user_uuid)
        except CustomUser.DoesNotExist:
            return False

        try:
            task = Tasks.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            return False

        # if task not in current sequence => this task in other sequence
        try:
            self.tasks.remove(str(task.id))
        except ValueError as e:
            prev_tasks_seq = TasksSeq.objects.get(column=task.column)
            prev_tasks_seq.id_delete(task.id)
            task.column = self.column
            task.save()

        if prev_task_uuid:
            prev_task = Tasks.objects.get(uuid=prev_task_uuid)
            self.tasks.insert(self.tasks.index(str(prev_task.id))+1, str(task.id))
        else:
            self.tasks.insert(0, str(task.id))

        self.save()

        return True

class Chat(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True)

    objects = None

    def __str__(self) -> str:
        return '{} Chat'.format(self.project.name)

class Message(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    message_content = models.CharField(max_length=120, blank=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)
    writer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    objects = None

    def __str__(self) -> str:
        return '{} | {}'.format(self.chat.project.name, self.message_content[:20])

# All Signals

# User signals
def pre_save_user_dispatcher(sender, **kwargs):
    kwargs['instance'].username = '{} {}'.format(kwargs['instance'].first_name, kwargs['instance'].second_name)

# Project signals
def post_save_project_member_creator(sender, **kwargs):
    if kwargs['created']:
        new_member_pool = MemberPool(project=kwargs['instance'])
        new_member_pool.save()
        new_member_pool.members.add(kwargs['instance'].owner)

def post_save_project_chat_creator(sender, **kwargs):
    if kwargs['created']:
        new_chat = Chat(project=kwargs['instance'])
        new_chat.save()

def pre_delete_task_delete_from_seq(sender, **kwargs):
    tasks_seq = TasksSeq.objects.get(column=kwargs['instance'].column)
    tasks_seq.delete_task_from_seq(kwargs['instance'].id)
    tasks_seq.save()

def post_save_task_add_to_seq(sender, **kwargs):
    if kwargs['created']:
        tasks_seq = TasksSeq.objects.get(column=kwargs['instance'].column)
        tasks_seq.add_task_to_seq(kwargs['instance'].id)
        tasks_seq.save()

def post_save_column_tasks_seq_creator(sender, **kwargs):
    if kwargs['created']:
        tasks_seq = TasksSeq(tasks=[], column=kwargs['instance'])
        tasks_seq.save()


post_save.connect(post_save_project_member_creator, sender=Project)
post_save.connect(post_save_project_chat_creator, sender=Project)
pre_save.connect(pre_save_user_dispatcher, sender=CustomUser)
pre_delete.connect(pre_delete_task_delete_from_seq, sender=Task)
post_save.connect(post_save_task_add_to_seq, sender=Task)
post_save.connect(post_save_column_tasks_seq_creator, sender=Column)
