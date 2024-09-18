import requests

from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms

from config import settings


class UserSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        field_classes = {'username': UsernameField, 'email': forms.EmailField}

    def is_valid(self):
        # parent validation
        if not super(UserCreationForm, self).is_valid():
            return False

        # captcha
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': self.data.get('g-recaptcha-response')
        }

        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=values)
        result = r.json()

        if not result.get('success'):
            self.add_error(None, 'CAPTCHA_FIELD_ERR_YOU_ARE_A_ROBOT')
            return False

        # EOF recaptcha validation

        return True
