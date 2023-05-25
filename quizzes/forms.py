from .models import User, Quiz
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


class QuizForm(ModelForm):

    class Meta:
        model = Quiz
        fields = ['name', 'topic']
        labels = {'name': '', 'topic': ''}

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Quiz Name', 'name': 'name'})

        self.fields['topic'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Topic', 'name': 'topic'})
