from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from django.contrib.auth.decorators import login_required


def index(request):

    if request.user.is_authenticated:
        return redirect('account')
  
    form = UserForm()

    if request.method == 'POST':

        form = UserForm(request.POST)

        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
          
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('index')
        
    return render(request, 'quizzes/index.html', {
        'form': form
    })



@login_required(login_url='index')
def account(request):
    return render(request, 'quizzes/account.html')