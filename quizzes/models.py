from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    account_color = models.CharField(max_length=6, unique=True)
    joined = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.username


class Quiz(models.Model):

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200, blank=True, null=True)
    pin = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Participant(models.Model):

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    account_color = models.CharField(max_length=6, unique=True)
    quizzes = models.ManyToManyField(Quiz, default=None)
    user_id = models.UUIDField(User.id, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Question(models.Model):

    ANSWER_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    )

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    choice_A = models.CharField(max_length=100)
    choice_B = models.CharField(max_length=100)
    choice_C = models.CharField(max_length=100)
    choice_D = models.CharField(max_length=100)
    answer_key = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    points = models.PositiveIntegerField(default=1)
    seconds = models.PositiveIntegerField(
        default=5, validators=[MinValueValidator(5), MaxValueValidator(180)])
    is_active = models.BooleanField(default=False)
    number = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.question

    def serialize(self):
        return {
            "id": self.id,
            "question": self.question,
            "choice_A": self.choice_A,
            "choice_B": self.choice_B,
            "choice_C": self.choice_C,
            "choice_D": self.choice_D,
            "answer_key": self.answer_key,
            "points": self.points,
            "seconds": self.seconds,
            "number": self.number
        }


class Answer(models.Model):

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_key = models.CharField(max_length=1)
    seconds = models.PositiveIntegerField()
    score = models.PositiveIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['seconds']

    def __str__(self):
        return f'answer: {self.answer_key}'

    def serialize(self):
        return {
            "id": self.id,
            "participant": {
                "id": self.participant.id,
                "name": self.participant.name,
                "account_color": self.participant.account_color,
                "user_id": self.participant.user_id,
                "joined": self.participant.joined.strftime("%b %d %Y, %I:%M %p")
            },
            "question": self.question.id,
            "answer_key": self.answer_key,
            "seconds": self.seconds,
            "score": self.score,
            "submitted": self.submitted.strftime("%b %d %Y, %I:%M %p")
        }
