from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserForm, QuizForm, QuestionForm
from django.contrib.auth.decorators import login_required, user_passes_test
import random
from .models import Quiz, Participant, Question, Answer
from django.http import JsonResponse
import json
from django.db.utils import IntegrityError


def index(request):

    if request.user.is_authenticated:
        return redirect('account', 'all')

    if request.method == 'POST':

        form = UserForm(request.POST)

        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account', 'all')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('index')

    else:
        form = UserForm()

    return render(request, 'quizzes/index.html', {
        'form': form
    })


def register(request):

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.username = request.POST['username'].lower()
            user.password = make_password(user.password)

            # Generate a random number in between 0 and 2^24
            account_color = random.randrange(0, 2**24)

            # Convert that number from base-10 (decimal) to base-16 (hexadecimal)
            hex_color = hex(account_color)

            account_color = hex_color[2:]
            user.account_color = account_color

            user.save()

            login(request, user)
            return redirect('account', 'all')

        else:
            messages.error(request, 'Try a different username')
            return redirect('register')

    else:
        form = UserForm()

    return render(request, 'quizzes/register.html', {
        'form': form
    })


@login_required(login_url='index')
def logout_view(request):
    logout(request)
    return redirect("index")


@login_required(login_url='index')
def account(request, search_option='all'):

    user = request.user

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    quizzes = []

    if search_option == 'participant':
        try:
            quizzes = Participant.objects.get(user_id=user.id).quizzes
            quizzes = quizzes.filter(name__icontains=search_query)
        except Participant.DoesNotExist:
            pass
    elif search_option == 'host':
        try:
            quizzes = Quiz.objects.filter(host=user)
            quizzes = quizzes.filter(name__icontains=search_query)
        except Quiz.DoesNotExist:
            pass
    else:
        try:
            quizzes = Quiz.objects.all()
            quizzes = quizzes.filter(name__icontains=search_query)
        except Quiz.DoesNotExist:
            pass

    return render(request, 'quizzes/account.html', {
        'user': user,
        'quizzes': quizzes,
        'option': search_option,
        'search_query': search_query
    })


def join_quiz(request):

    if request.method == 'POST':

        if request.user.is_authenticated:
            name = request.user.name
        else:
            name = request.POST['name']

        pin = request.POST['pin']
        quiz = None

        try:
            quiz = Quiz.objects.get(pin=pin)
        except (Quiz.DoesNotExist, ValueError):
            messages.error(request, 'Invalid PIN')

        if quiz:

            color = hex(random.randrange(0, 2**24))
            account_color = color[2:]

            participant = Participant(
                name=name, account_color=account_color, is_active=True)
            participant.save()
            participant.quizzes.add(quiz)

            if request.user.is_authenticated:
                user_id = request.user.id
                participant.user_id = user_id

            participant.save()
            return redirect('live_quiz', pin, participant.id)

    return render(request, 'quizzes/join-quiz.html')


def live_quiz(request, pin, participant_id):

    try:
        quiz = Quiz.objects.get(pin=pin)
        participant = Participant.objects.get(id=participant_id)
    except (Quiz.DoesNotExist, Participant.DoesNotExist):         
        return redirect('index')

    if quiz and participant:

        try:
            question = Question.objects.get(quiz=quiz, is_active=True)
        except Question.DoesNotExist:
            question = None

        if request.method == 'POST':

            data = json.loads(request.body)

            key = data.get('answer')
            countdown = data.get('seconds')
            seconds = question.seconds - countdown

            if key.lower() == question.answer_key.lower():
                score = int(
                    (question.points*countdown)/question.seconds)
            else:
                score = 0

            answer = Answer(participant=participant, question=question,
                            answer_key=key, seconds=seconds, score=score)
            answer.save()

    return render(request, 'quizzes/live-quiz.html', {
        'participant': participant,
        'quiz': quiz,
        'question': question
    })


@login_required(login_url='index')
def create_quiz(request):

    if request.method == 'POST':

        form = QuizForm(request.POST)

        if form.is_valid():

            quiz = form.save(commit=False)
            quiz.host = request.user

            while True:
                try:
                    quiz.pin = random.randint(1000, 9999)
                    quiz.save()
                    break
                except IntegrityError:
                    print('UNIQUE constraint failed: quizzes_quiz.pin')

            return redirect('edit_quiz', quiz.id)

    else:
        form = QuizForm()

    return render(request, 'quizzes/create-quiz.html', {
        'form': form
    })


@login_required(login_url='index')
def edit_quiz(request, id):

    quiz = Quiz.objects.get(id=id)

    if quiz.host == request.user:

        questions = Question.objects.filter(quiz=quiz)

        if request.method == 'POST' and 'edit-quiz' in request.POST:

            quiz_form = QuizForm(request.POST, instance=quiz)

            if quiz_form.is_valid():
                quiz_form.save()

        else:
            quiz_form = QuizForm(instance=quiz)

        if request.method == 'POST' and 'add-question' in request.POST:

            question_form = QuestionForm(request.POST)

            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.save()

                return redirect('edit_quiz', id)

        else:
            question_form = QuestionForm()

        return render(request, 'quizzes/edit-quiz.html', {
            'quiz_form': quiz_form,
            'question_form': question_form,
            'questions': questions,
            'quiz': quiz
        })


@login_required(login_url='index')
def question(request, id):

    question = Question.objects.get(id=id)

    if question.quiz.host == request.user:

        if request.method == 'PUT':

            data = json.loads(request.body)

            if data.get('is_active'):

                Question.objects.update(is_active=False)
                question.is_active = True
                question.number = data.get('number')
                question.save()
               
            else:
                question.question = data.get('question_text')
                question.choice_A = data.get('option_a')
                question.choice_B = data.get('option_b')
                question.choice_C = data.get('option_c')
                question.choice_D = data.get('option_d')
                question.answer_key = data.get('answer_key')
                question.points = data.get('points')
                question.seconds = data.get('seconds')

            question.save()

            return HttpResponse(status=204)

        elif request.method == 'DELETE':
            question.delete()
            return HttpResponse(status=204)

        else:
            return JsonResponse(question.serialize())


@login_required(login_url='index')
def delete_quiz(request, id):

    quiz = Quiz.objects.get(id=id)

    if quiz.host == request.user:
        quiz.delete()

        return HttpResponse(status=204)


@login_required(login_url='index')
def start_quiz(request, id):

    quiz = Quiz.objects.get(id=id)

    if quiz.host == request.user:
            
            if request.method == 'PUT':

                data = json.loads(request.body)

                if data.get('is_active') == False:

                    quiz.is_active = False
                    quiz.participant_set.update(is_active=False)
                    quiz.save()

                    while True:
                        try:
                            quiz.pin = random.randint(1000, 9999)
                            quiz.save()
                            break
                        except IntegrityError:
                            print('UNIQUE constraint failed: quizzes_quiz.pin')
                   

                    return HttpResponse(status=204)
                
                
            else:
                quiz.is_active = True
                quiz.save()
                Question.objects.update(is_active=False)  
                questions = Question.objects.filter(quiz=quiz)
                num_participants = quiz.participant_set.filter(is_active=True).count()

                return render(request, 'quizzes/start-quiz.html', {
                        'questions': questions,
                        'quiz': quiz,
                        'num_participants': num_participants
                    })


