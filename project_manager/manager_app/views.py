from django.shortcuts import render, redirect
from django.http import HttpResponse

# Local imports
from .models import CustomUser
from .forms import RegistrationForm

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
