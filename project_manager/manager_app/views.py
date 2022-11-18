from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import (
        authenticate,
        login,
        logout,
        )
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from django.contrib.auth.views import PasswordResetConfirmView

# Local imports
from .models import (
        CustomUser,
        Avatar
        )
from .forms import (
        RegistrationForm,
        LoginForm,
        NewPasswordSetForm,
        )
from .decorators import (
        anonymous_required
        )

def get_error_messages(form) -> dict:
    error_dict = dict()
    invalid_field = ''

    for field in form.errors:
        error_dict[field] = form.errors[field][0]

    invalid_field = [x for x in form.errors.as_data()]

    return {'invalid_field': invalid_field[0], 'error_dict': error_dict}

def main_page(request): 
    return render(request, 'manager_app/title_page.html', {})

@anonymous_required
def registration_page(request):
    ModelFormSet = RegistrationForm
    form = ModelFormSet

    context = {
            'form': form,
            }

    if request.method == 'POST':
        form = ModelFormSet(request.POST)

        if form.is_valid():
            form.save() 
            return redirect(reverse('title_page'))

        error_messages = get_error_messages(form)
        
        context['form'] = form
        context['invalid_field'] = error_messages['invalid_field']
        context['error_dict'] = error_messages['error_dict']

    return render(request, 'manager_app/registration_page.html', context)

@anonymous_required
def login_page(request):
    ModelFormSet = LoginForm
    form = ModelFormSet
    
    context = {'form': form}

    if request.method == 'POST':

        form = ModelFormSet(request.POST)
        user = authenticate(email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)

            return redirect(reverse('title_page'))
        
        context['form'] = form
        context['invalid_field'] = 'all'
        context['error_dict'] = {'all': 'Wprowadzono błędne dane'}

    return render(request, 'manager_app/login_page.html', context)

def logout_page(request):

    logout(request)

    return redirect(reverse('login_page'))

@login_required(login_url='login/')
def account_info_page(request):
    
    mode = request.GET.get('mode', '')
    avatar_slug = request.GET.get('avatar', '')

    if mode == 'change':
        cur_user = CustomUser.objects.get(id=request.user.id)
        try:
            cur_user.user_avatar = Avatar.objects.get(search_slug=avatar_slug)
        except Avatar.DoesNotExist:
            return redirect(reverse('account_info_page'))
        cur_user.save()

        return redirect(reverse('account_info_page'))

    avatars = Avatar.objects.all()
    avatar_change_url = '{}{}'.format(reverse('account_info_page'), '?mode=change&avatar=') 

    context = {
            'avatars': avatars,
            'avatar_change_url': avatar_change_url,
            }

    return render(request, 'manager_app/account_info_page.html', context)


class PasswordResetConfirmViewWithErrors(PasswordResetConfirmView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':

            form = context['form']

            if form.is_valid():
                context['invalid_field'] = ''
                context['error_dict'] = {}
            else:
                error_messages = get_error_messages(form)

                context['invalid_field'] = error_messages['invalid_field']
                context['error_dict'] = error_messages['error_dict']

        return context

