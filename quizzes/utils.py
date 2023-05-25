from .models import Quiz


def validate_pin(pin):

    quiz = Quiz.objects.get(pin=pin)

    return quiz
