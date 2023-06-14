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
            {'class': 'input', 'placeholder': 'Nombre', 'name': 'name', 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})
        self.fields['username'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Usuario', 'name': 'username', 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})
        self.fields['password'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Contraseña', 'name': 'password', 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})


class QuizForm(ModelForm):

    class Meta:
        model = Quiz
        fields = ['name', 'topic']
        labels = {'name': '', 'topic': ''}

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'id': 'name', 'class': 'input', 'placeholder': 'Nombre del quiz', 'name': 'name', 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['topic'].widget.attrs.update(
            {'id': 'input', 'class': 'input', 'placeholder': 'Categoría', 'name': 'topic'})


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
            {'id': 'question', 'class': 'input', 'placeholder': 'Teclee la pregunta', 'name': 'question', 'required': True, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['choice_A'].widget.attrs.update(
            {'id': 'choice_a', 'class': 'input choice_a', 'placeholder': 'Teclee posible respuesta', 'name': 'choice_a', 'required': True, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['choice_B'].widget.attrs.update(
            {'id': 'choice_b', 'class': 'input choice_b', 'placeholder': 'Teclee posible respuesta', 'name': 'choice_b', 'required': True, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['choice_C'].widget.attrs.update(
            {'id': 'choice_c', 'class': 'input choice_c', 'placeholder': 'Teclee posible respuesta', 'name': 'choice_c', 'required': True, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['choice_D'].widget.attrs.update(
            {'id': 'choice_d', 'class': 'input choice_d', 'placeholder': 'Teclee posible respuesta', 'name': 'choice_d', 'required': True, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['answer_key'].widget.attrs.update(
            {'id': 'answer_key', 'class': 'input', 'placeholder': 'Seleccione la respuesta correcta', 'name': 'answer_key', 'required': True, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['points'].widget.attrs.update(
            {'id': 'points', 'class': 'input', 'placeholder': 'Puntos', 'name': 'points', 'min': 1, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})

        self.fields['seconds'].widget.attrs.update(
            {'id': 'seconds', 'class': 'input', 'placeholder': 'Tiempo límite en segundos', 'name': 'seconds', 'min': 5, 'oninvalid': 'this.setCustomValidity("Por favor, complete la información")'})
