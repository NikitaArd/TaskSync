from django.urls import path

from .views import (
        main_page,
        registration_page,
        )

urlpatterns = [
        path('', main_page, name='mane_page'),
        path('registration/', registration_page, name='registration_page')
]
