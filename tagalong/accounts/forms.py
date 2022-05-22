from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
import logging
from django.core.validators import MinLengthValidator

logger = logging.getLogger("mylogger")


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username',  'first_name', 'last_name',
                  'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email','profile_img','friends')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Namn på Swish-betalare', 'style': 'height: 40px; width: 300px;  padding: 7px; margin-bottom: 10px; font-size: 15px;', 'required': True})
        self.fields['first_name'].label = "Förnamn:"

        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Namn på Swish-betalare', 'style': 'height: 40px; width: 300px;  padding: 7px; margin-bottom: 10px; font-size: 15px;', 'required': True})
        self.fields['last_name'].label = "Efternamn:"

        self.fields['email'].disabled = True
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '', 'style': 'height: 40px; width: 300px;  padding: 7px; margin-bottom: 10px; font-size: 15px;'})
        self.fields['email'].label = "Email:"
