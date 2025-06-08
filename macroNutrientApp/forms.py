from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Register  # Import your user model

class RegisterForm(UserCreationForm):
    class Meta:
        model = Register  # Use your custom user model
        fields = ["username", "email", "password1", "password2"]