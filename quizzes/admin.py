from django.contrib import admin
from .models import User, Quiz, Question, Answer, Participant

admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Participant)

