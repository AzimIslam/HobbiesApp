from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from mainapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponseNotFound

# Create your views here.

def login_view(request):
    '''
    This view renders the login page
    '''

    if request.user.is_authenticated:
        return render(request, "mainapp/profile/homepage.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # Change to homepage
            auth.login(request, user)
            return render(request, "mainapp/profile/homepage.html")
        else:
            return render(request, 'mainapp/login.html', {
                'title': 'Login Page',
                'fail': True
            })
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

            createdUser = auth.authenticate(request, username=username, password=request.POST.get("password"))
            auth.login(request, createdUser)

            return render(request, "mainapp/profile/homepage.html")
        else:
            return render(request, 'mainapp/signup.html', {
                'title': 'Create an account'
            })


@login_required
def create_hobbies_view(request):
    return render(request, 'mainapp/profile/createhobbies.html')

@login_required
def search_hobbies_view(request):
    return render(request, 'mainapp/profile/searchhobbies.html')

@login_required
def home_view(request):
    return render(request, 'mainapp/profile/homepage.html')

@login_required
def social_view(request):
    return render(request, 'mainapp/profile/social.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def user_profile_view(request, username):
    print("running")
    try:
        user = User.objects.get(username=username)
        json_obj = user.to_dict()
        requestSent = False
        try:
            requestSent = FriendRequest.objects.get(from_user=request.user, to_user=user)
            requestSent = True
        except:
            pass
        return render(request, 'mainapp/profile/profile.html', {
            'profile': json_obj,
            'requestSent': requestSent,
        })
    except User.DoesNotExist:
        return HttpResponseNotFound("User not found")


