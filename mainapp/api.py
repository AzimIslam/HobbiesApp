
import json

from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def hobbie_api(request):
    if request.method == "POST":
        try:
            print("POOOOOOO")
            body_unicode = request.body.decode('utf8')
            body = json.loads(body_unicode)
            newHobbie = Hobby(
                name = body["hobbieName"],
                description = body["hobbieDescription"],
            )
            newHobbie.save()
            print("SUCESSSS")
            return JsonResponse({})
        except:
            return HttpResponseNotFound("New Hobbie Not created")
