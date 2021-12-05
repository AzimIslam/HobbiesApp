from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from mainapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Create your views here.

def login_view(request):
    '''
    This view renders the login page
    '''

    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Change to homepage
            login(request, user)
            print("Successful login")
            return redirect("/home")
        else:
            print("Unsuccessful")
            return JsonResponse({"success": False})
    else:
        return render(request, 'mainapp/login.html', {
            'title': 'Login Page'
        })

def register_view(request):
        if request.method == 'POST':
            email = request.POST.get("email")
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            surname = request.POST.get("surname")
            password = make_password(request.POST.get("password"))
            dateofbirth = request.POST.get("dob")

            user = User(email=email, username=username, first_name=first_name, last_name=surname, password=password, date_of_birth=dateofbirth)
            user.save()

            createdUser = authenticate(request, username=username, password=request.POST.get("password"))
            login(request, createdUser)

            return redirect("/home")
        else:
            return render(request, 'mainapp/signup.html', {
                'title': 'Create an account'
            })

@login_required
def home_view(request):
    return render(request, 'mainapp/profile/homepage.html')