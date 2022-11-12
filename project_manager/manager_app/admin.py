from django.contrib import admin

# local imports
from .models import (
        CustomUser,
        Avatar,
        )

admin.site.register(CustomUser)
admin.site.register(Avatar)
