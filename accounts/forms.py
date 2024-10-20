from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email