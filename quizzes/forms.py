from .models import User, Quiz, Question
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
            {'id': 'name', 'class': 'input', 'placeholder': 'Quiz Name', 'name': 'name'})

        self.fields['topic'].widget.attrs.update(
            {'id': 'input', 'class': 'input', 'placeholder': 'Topic', 'name': 'topic'})


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('quiz', 'is_active',)
        labels = {'question': '', 'choice_A': '',
                  'choice_B': '', 'choice_C': '', 'choice_D': '', 'answer_key': '', 'points': '', 'seconds': ''}

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.attrs.update(
            {'id': 'question', 'class': 'input', 'placeholder': 'Type a question', 'name': 'question', 'required': True})

        self.fields['choice_A'].widget.attrs.update(
            {'id': 'choice_a', 'class': 'input choice_a', 'placeholder': 'Type choice', 'name': 'choice_a', 'required': True})

        self.fields['choice_B'].widget.attrs.update(
            {'id': 'choice_b', 'class': 'input choice_b', 'placeholder': 'Type choice', 'name': 'choice_b', 'required': True})

        self.fields['choice_C'].widget.attrs.update(
            {'id': 'choice_c', 'class': 'input choice_c', 'placeholder': 'Type choice', 'name': 'choice_c', 'required': True})

        self.fields['choice_D'].widget.attrs.update(
            {'id': 'choice_d', 'class': 'input choice_d', 'placeholder': 'Type choice', 'name': 'choice_d', 'required': True})

        self.fields['answer_key'].widget.attrs.update(
            {'id': 'answer_key', 'class': 'input', 'placeholder': 'Choose correct answer', 'name': 'answer_key', 'required': True})

        self.fields['points'].widget.attrs.update(
            {'id': 'points', 'class': 'input', 'placeholder': 'Enter points', 'name': 'points', 'min': 1})

        self.fields['seconds'].widget.attrs.update(
            {'id': 'seconds', 'class': 'input', 'placeholder': 'Enter number of seconds', 'name': 'seconds', 'min': 5})
