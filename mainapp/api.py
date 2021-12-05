from django.contrib.auth.hashers import make_password
import json
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest

from .models import User

def register_api(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf8')
        body_data = json.loads(body_unicode)

        email = body_data["email"]
        username = body_data["username"]
        first_name = body_data["first_name"]
        surname = body_data["surname"]
        password = make_password(body_data["password"])
        dateofbirth = body_data["dob"]

        user = User(email=email, username=username, first_name=first_name, last_name=surname, password=password, date_of_birth=dateofbirth)
        user.save()
        
        return JsonResponse({})
    
    return HttpResponseBadRequest("Bad Request")

