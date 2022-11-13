from django.shortcuts import render, redirect
from django.http import HttpResponse

# Local imports
from .models import CustomUser
from .forms import RegistrationForm

def main_page(request): 
    return render(request, 'manager_app/title_page.html', {})

def registration_page(request):
    ModelFormSet = RegistrationForm

    if request.method == 'POST':
        form = ModelFormSet(request.POST)

        if form.is_valid():
            form.save() 
            return redirect('/')

    form = ModelFormSet
    
    return render(request, 'manager_app/registration_page.html', {'form': form})
