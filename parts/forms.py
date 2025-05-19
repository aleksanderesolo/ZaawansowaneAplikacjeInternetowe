from django import forms
from .models import Part
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profil
from .models import Samochod

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        widgets = {
            'samochody': forms.CheckboxSelectMultiple
        }
        exclude = ['autor']

from .models import PartDetails

class PartDetailsForm(forms.ModelForm):
    class Meta:
        model = PartDetails
        fields = '__all__'

from .models import Ocena

class OcenaForm(forms.ModelForm):
    class Meta:
        model = Ocena
        fields = ['ocena', 'komentarz']


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, label="Adres e-mail")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten adres e-mail jest już używany.")
        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['imie', 'nazwisko', 'opis', 'avatar']

class SamochodForm(forms.ModelForm):
    class Meta:
        model = Samochod
        fields = ['marka', 'model', 'rok']
