from django.contrib.auth.forms import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Imię')
    first_name.widget.attrs.update({
        'type':'input',
        'class':'field-input',
        'placeholder':'Imię',
        'name':'name',
        'id':'name',
        'required':'required',
        })
    
    second_name = forms.CharField(label='Nazwisko')
    second_name.widget.attrs.update({
        'type':'input',
        'class':'field-input',
        'placeholder':'Nazwisko',
        'name':'second-name',
        'id':'second-name',
        'required':'required',
        })

    email = forms.EmailField(label='E-mail')
    email.widget.attrs.update({
        'type':'email',
        'class':'field-input',
        'placeholder':'Email',
        'name':'email',
        'id':'email',
        'required':'required',
        })

    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={
        'type':'password',
        'class':'field-input',
        'placeholder':'Hasło',
        'name': 'password1',
        'id':'password1',
        'required': 'required',
        }))

    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={
        'type':'password',
        'class':'field-input',
        'placeholder':'Powtórz hasło',
        'name': 'password2',
        'id':'password2',
        'required': 'required',
        }))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'second_name', 'email', 'password1', 'password2']
