from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import (
        CustomPasswordResetForm,
        NewPasswordSetForm,
        )

from .views import (
        main_page,
        registration_page,
        login_page,
        logout_page,
        account_info_page,
        projects_menu,
        PasswordResetConfirmViewWithErrors
        )

urlpatterns = [
        path('', main_page, name='title_page'),
        path('registration/', registration_page, name='registration_page'),
        path('login/', login_page, name='login_page'),
        path('logout/', logout_page, name='logout'),
        path('accounts/information/', account_info_page, name='account_info_page'),
        path('menu/', projects_menu, name='projects_menu'),

        # Password reset URLs

        path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
            template_name='manager_app/auth_templates/reset_password.html',
            form_class=CustomPasswordResetForm,
            email_template_name='manager_app/auth_templates/emails/reset_email.txt',
            ), name='password_reset'),
        
        path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='manager_app/auth_templates/reset_password_done.html',
            ), name='password_reset_done'),
        
        path('accounts/password_reset/<uidb64>/<token>/', PasswordResetConfirmViewWithErrors.as_view(
            template_name='manager_app/auth_templates/reset_password_confirm.html',
            form_class=NewPasswordSetForm,
            ), name='password_reset_confirm'),
        
        path('accounts/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='manager_app/auth_templates/reset_password_complete.html',
            ), name='password_reset_complete'),
]
