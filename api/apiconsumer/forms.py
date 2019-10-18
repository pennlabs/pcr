from django import forms
from .models import APIConsumer


class TokenForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text='Required')
    email = forms.EmailField(max_length=75, help_text='Required')
    description = forms.CharField()

    class Meta:
        model = APIConsumer
        fields = ('name', 'email', 'description')


class ResetTokenForm(forms.Form):
    email = forms.EmailField(max_length=75, help_text='Required')
