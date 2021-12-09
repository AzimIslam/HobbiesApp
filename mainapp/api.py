
import json
from django.core.exceptions import BadRequest

from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404


from .models import *

@login_required
def profile_api(request):
    user = get_object_or_404(User, username=request.user)
    if request.method == "PUT":
        body_unicode = request.body.decode('utf8')
        body = json.loads(body_unicode)

        name = body["name"].split(" ")
        dob = body["dob"]
        city = body["city"]
        email = body["email"]
        print(name)

        if len(name) != 2:
            return HttpResponseBadRequest({'error': 'Please enter a your first name and surname seperated by spaces'})

        user.first_name = name[0]
        user.last_name = name[1]
        user.date_of_birth = dob
        user.email = email
        user.city = city

        user.save()
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

@login_required
def hobby_api(request, hobby_name):
    try:
        hobby = Hobby.objects.get(name=hobby_name)
        json_obj = hobby.to_dict()
        return render(request, 'mainapp/profile/hobby.html', {
            'hobby': json_obj
        })
    except Hobby.DoesNotExist:
        return HttpResponse(f"Invalid Hobby: {hobby_name}")

@login_required
def user_profile_api(request, username):
    try:
        user = User.objects.get(username=username)
        json_obj = user.to_dict()
        return render(request, 'mainapp/profile/profile.html', {
            'profile': json_obj
        })
    except User.DoesNotExist:
        return HttpResponseNotFound("User not found")

@login_required
def hobbies_api(request):
    return JsonResponse({
        'hobbies': [
        hobby.to_dict()
        for hobby in Hobby.objects.all()
        ]
    })

@login_required
def user_hobbies_api(request):
    user = get_object_or_404(User, username=request.user)
    return JsonResponse({"dict": user.get_hobbies()})

@login_required
def user_delete_hobby(request):
    user = get_object_or_404(User, username=request.user)
    if request.method == "DELETE":
        body_unicode = request.body.decode('utf8')
        body = json.loads(body_unicode)

        hobbyName = body["hobby_name"]

        hobby = get_object_or_404(Hobby, name=hobbyName)
        user.hobbies.remove(hobby)

        return JsonResponse({"dict": user.get_hobbies()})

@login_required
def uploadFiles(request):
    user = get_object_or_404(User, username=request.user)

    if 'profile_pic' in request.FILES:
        user.profile_pic = request.FILES['profile_pic']
        user.save()
        return JsonResponse({'profile_pic': user.profile_pic.url})
    else:
        raise Http404('Image file not received')

@login_required
def toggle_hobby(request):
    if request.method == "PUT":
        try:
            user = get_object_or_404(User, username=request.user)
            body_unicode = request.body.decode('utf8')
            body = json.loads(body_unicode)
            hobby = get_object_or_404(Hobby, name=body['hobby_name'])
            if (body['exisitng_hobby']):
                user.hobbies.remove(hobby)
            else:
                user.hobbies.add(hobby)
            user.save()
            return JsonResponse({"added": body['exisitng_hobby']})
        except:
            return HttpResponseNotFound("Hobby Not Added")
