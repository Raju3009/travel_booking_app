from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["num_seats"]
        widgets = {
            "num_seats": forms.NumberInput(attrs={"min": 1})
        }
