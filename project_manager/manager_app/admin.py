from django.contrib import admin

# local imports
from .models import (
        CustomUser,
        Avatar,
        Project,
        )

admin.site.register(CustomUser)
admin.site.register(Avatar)
admin.site.register(Project)
