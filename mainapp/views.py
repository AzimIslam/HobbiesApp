from django.shortcuts import render

# Create your views here.

def login_view(request):
    '''
    This view renders the login page
    '''
    return render(request, 'mainapp/login.html', {
        'title': 'Login Page'
    })

def register_view(request):
    return render(request, 'mainapp/signup.html', {
        'title': 'Create an account'
    })