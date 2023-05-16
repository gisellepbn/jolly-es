from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    account_color = models.CharField(max_length=6, unique=True)
    joined = models.DateTimeField(auto_now_add=True, editable=False)


    def __str__(self):
        return self.name
    


class Quiz(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    host = models.ForeignKey(User, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=200, blank=True, null=True)
    pin = models.PositiveIntegerField(unique=True, min=1000, max=9999)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    


class Participant:

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    account_color = models.CharField(max_length=6, unique=True)
    quizzes = models.ManyToManyField(Quiz)
    user_id = models.UUIDField(User.id, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['name']
        

    def __str__(self):
        return self.name



class Question(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    choice_A = models.CharField(max_length=100)
    choice_B = models.CharField(max_length=100)
    choice_C = models.CharField(max_length=100)
    choice_D = models.CharField(max_length=100)
    answer_key = models.CharField(max_length=1)
    points = models.PositiveIntegerField(min=1)
    time = models.TimeField()
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)


    class Meta:
        ordering = ['created']


    def __str__(self):
        return self.question



