from django.contrib import admin

# local imports
from .models import (
        CustomUser,
        Avatar,
        Project,
        MemberPool,
        Column,
        Task,
        TasksSeq,
        Chat,
        Message,
        )

# User models
admin.site.register(CustomUser)
admin.site.register(Avatar)

# Project models
admin.site.register(Project)
admin.site.register(MemberPool)
admin.site.register(Column)
admin.site.register(Task)
admin.site.register(TasksSeq)

# Chat models
admin.site.register(Chat)
admin.site.register(Message)
