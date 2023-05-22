from .models import User, Participant
from django.forms import ModelForm, PasswordInput


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['name', 'username', 'password']
        labels = {
            'name': '', 'username': '', 'password': '',
        }

        help_texts = {
            "username": None,
        }

        widgets = {
            'password': PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Name', 'name': 'name'})
        self.fields['username'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Username', 'name': 'username'})
        self.fields['password'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Password', 'name': 'password'})
