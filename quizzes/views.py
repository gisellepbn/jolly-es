from django.shortcuts import render

def index(request):
    return render(request, 'quizzes/index.html')
