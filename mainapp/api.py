
import json

from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import *

@login_required
def profile_api(request):
    print(request.user)
    user = get_object_or_404(User, username=request.user)
    return JsonResponse({'user': user.to_dict()})

@login_required
def hobbie_api(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf8')
            body = json.loads(body_unicode)
            newHobbie = Hobby(
                name = body["hobbieName"],
                description = body["hobbieDescription"],
            )
            newHobbie.save()
            return JsonResponse({})
        except:
            return HttpResponseNotFound("New Hobbie Not created")
