from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.add_message(request, constants.ERROR, "Passwords don't match. Please try again.")
            return redirect('/users/signup/')
        
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, "Password should have more than 6 characters. Please try again.")
            return redirect('/users/signup/')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, "Username already taken. Please try different one.")
            return redirect('/users/signup/')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password, 
            )

        return redirect('/users/login')


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/patients/home')

        messages.add_message(request, constants.ERROR, 'Username or password incorrect. Please try again.')
        return redirect('/users/login')
    
def logout(request):
    auth.logout(request)
    return redirect('/users/login')