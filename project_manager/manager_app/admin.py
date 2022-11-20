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
        )

admin.site.register(CustomUser)
admin.site.register(Avatar)
admin.site.register(Project)
admin.site.register(MemberPool)
admin.site.register(Column)
admin.site.register(Task)
admin.site.register(TasksSeq)
