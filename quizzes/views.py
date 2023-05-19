from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import random


def index(request):

    if request.user.is_authenticated:
        return redirect('account')
  
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
 
            account_color = "#" + hex_color[2:]
            user.account_color = account_color

            user.save()  

            login(request, user)
            return redirect('account')
                
        else:
            messages.error(request, 'Try a different username')
            return redirect('register')     
                

    else:
        form = UserForm()

    return render(request, 'quizzes/register.html', {
        'form': form
    })



@login_required(login_url='index')
def account(request):
    return render(request, 'quizzes/account.html')