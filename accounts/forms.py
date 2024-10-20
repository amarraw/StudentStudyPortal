from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Add a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Add your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Add your last name.')

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email