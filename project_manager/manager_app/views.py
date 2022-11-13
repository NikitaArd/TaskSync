from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Local imports
from .models import (
        CustomUser,
        Avatar
        )
from .forms import (
        RegistrationForm,
        LoginForm,
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
            return redirect('/')

        error_messages = get_error_messages(form)
        
        context['form'] = form
        context['invalid_field'] = error_messages['invalid_field']
        context['error_dict'] = error_messages['error_dict']

    return render(request, 'manager_app/registration_page.html', context)

def login_page(request):
    ModelFormSet = LoginForm
    form = ModelFormSet
    
    context = {'form': form}

    if request.method == 'POST':

        form = ModelFormSet(request.POST)
        user = authenticate(email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)

            return redirect('/')
        
        context['form'] = form
        context['invalid_field'] = 'all'
        context['error_dict'] = {'all': 'Wprowadzono błędne dane'}

    return render(request, 'manager_app/login_page.html', context)

def account_info_page(request):
    avatars = Avatar.objects.all()

    return render(request, 'manager_app/account_info_page.html', {'avatars': avatars})
