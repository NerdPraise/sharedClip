from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _


class SignInForm(ModelForm):
    username = forms.CharField()
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    
    class Meta:
        fields = ("username", "password")
        model = None
