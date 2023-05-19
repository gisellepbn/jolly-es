from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User
from django.forms import ModelForm, PasswordInput


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['name', 'username', 'password']
        labels = {
            'name': '', 'username':'', 'password':'',
        }

        help_texts = {
            "username": None,
        }

        widgets = {
            'password': PasswordInput()
        }


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'input', 'placeholder': 'Name', 'name': 'name'})
        self.fields['username'].widget.attrs.update({'class':'input', 'placeholder': 'Username', 'name': 'username'})
        self.fields['password'].widget.attrs.update({'class':'input', 'placeholder': 'Password', 'name': 'password'})