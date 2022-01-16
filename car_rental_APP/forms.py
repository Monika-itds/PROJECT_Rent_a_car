from django import forms
from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Car, CarDealer, District, Customer, Orders, User
from django.contrib.auth.models import User

User = get_user_model()


def login_not_taken(login):
    if User.objects.filter(username=login):
        raise ValidationError("Podany login jest już zajęty")


class CarDealerRegistrationForm(forms.Form):
    login = forms.CharField(label="Login", validators=[login_not_taken])
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password_repeated = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)
    name = forms.CharField(label="Imię")
    surname = forms.CharField(label="Nazwisko")
    email = forms.EmailField(label="Email")
    is_car_dealer = forms.BooleanField(label="Dealer")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeated = cleaned_data.get("password_repeated")
        if password != password_repeated:
            raise forms.ValidationError("Hasła są różne!")
        return cleaned_data

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_car_dealer = True
        return user


class CustomerRegistrationForm(forms.Form):
    login = forms.CharField(label="Login", validators=[login_not_taken])
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password_repeated = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)
    name = forms.CharField(label="Imię")
    surname = forms.CharField(label="Nazwisko")
    email = forms.EmailField(label="Email")
    is_car_customer = forms.BooleanField(label="Customer")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeated = cleaned_data.get("password_repeated")
        if password != password_repeated:
            raise forms.ValidationError("Hasła są różne!")
        return cleaned_data

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        return user


class LoginForm(forms.Form):
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class CarAddForm(forms.Form):
    car_name = forms.CharField(label="Marka")
    color = forms.CharField(label="Kolor")
    dealer = forms.ModelChoiceField(queryset=CarDealer.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.all())
    capacity = forms.ChoiceField(choices=Car.CAR_CAPACITY, label="Ilość miejsc")
    is_available = forms.BooleanField(label="Dostępność")
    engine = forms.ChoiceField(choices=Car.CAR_ENGINES, label="Rodzaj silnika")
    ac = forms.BooleanField(label="Klimatyzacja")
    description = forms.CharField(label="Opis")


class CarSearchForm(forms.Form):
    district_name = forms.CharField(label="Nazwa dzielnicy")


class CarSearchResultsForm(forms.Form):
    car_name = forms.CharField(label="Marka")
    color = forms.CharField(label="Kolor")
    id = forms.CharField(label="ID")
    district_pincode = forms.ModelChoiceField(queryset=District.objects.all())
    capacity = forms.ChoiceField(choices=Car.CAR_CAPACITY, label="Ilość miejsc")
    engine = forms.ChoiceField(choices=Car.CAR_ENGINES, label="Rodzaj silnika")
    description = forms.CharField(label="Opis")
    dealer = forms.ModelChoiceField(queryset=CarDealer.objects.all())


# class CarDealerPortalForm(forms.Form):
#     first_name = forms.CharField(label='Imię')
#     last_name = forms.CharField(label='Nazwisko')
#     mobile = forms.CharField(label='Numer telefonu')
#     email = forms.CharField(label='Email')
#     district = forms.ModelChoiceField(queryset=District.objects.all())
#     wallet = forms.IntegerField(label='Stan konta')#kaska w PLN do liczenia
#
# class CustomerPortlaForm(forms.Form):
#     first_name = forms.CharField(label='Imię')
#     last_name = forms.CharField(label='Nazwisko')
#     mobile = forms.CharField(label='Numer telefonu')
#     email = forms.CharField(label='Email')
#     district = forms.ModelChoiceField(queryset=District.objects.all())


# ------

# class PasswordResetForm(forms.Form):
#     password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)
#
#  #   def clean(self):
#  #       cleaned_data = super().clean()
# #        if cleaned_data ['password1'] == ['password2']:
# #       return cleaned_data
