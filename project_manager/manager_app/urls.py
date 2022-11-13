from django.urls import path

from .views import (
        main_page,
        registration_page,
        login_page,
        )

urlpatterns = [
        path('', main_page, name='main_page'),
        path('registration/', registration_page, name='registration_page'),
        path('login/', login_page, name='login_page'),
]
