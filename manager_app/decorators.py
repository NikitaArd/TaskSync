from django.shortcuts import redirect

from django.conf import settings
from django.urls import reverse


def anonymous_required(func, *args, **kwargs):
    def check_anonymous(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(settings.ANONYMOUS_REDIRECT))

        return func(request, *args, **kwargs)
    return check_anonymous
