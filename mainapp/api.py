
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

    newUser = User.objects.get(username=user.username)
    return JsonResponse({'user': newUser.to_dict()})

@login_required
def hobbie_api(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf8')
            body = json.loads(body_unicode)

            if len(body["hobbieName"]) == 0 or len(body["hobbieDescription"]) == 0:
                return HttpResponseBadRequest("Please ensure that the fields contain data")

            newHobbie = Hobby(
                name = body["hobbieName"],
                description = body["hobbieDescription"],
            )
            newHobbie.save()

            return JsonResponse({})
        except:
            return HttpResponseBadRequest("Hobby already exists")

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


@login_required
def users_api(request):
    if request.method == "GET":
        logged_in_user = request.user.username
        users_not_friends_with = []
        num_common_hobbies_users = []
        for user in User.objects.all():
            if user.to_dict()["username"] == logged_in_user:
                continue
            else:
                friends_with_user = False
                for friend in user.friends.all():
                    if logged_in_user == friend.username:
                        friends_with_user = True
                        break
                if not friends_with_user:
                    not_friend_hobbies = user.hobbies.all()
                    logged_in_user_hobbies = request.user.hobbies.all()

                    common_hobbies = list(set(not_friend_hobbies).intersection(logged_in_user_hobbies))
                    num_common_hobbies = len(common_hobbies)

                    users_not_friends_with.append(user)
                    num_common_hobbies_users.append(num_common_hobbies)


        users_sent_requests_to = FriendRequest.objects.filter(from_user=request.user)

        return JsonResponse({
            'users_not_friends_with': [user.to_dict() for user in users_not_friends_with],
            'common_hobbies': [number for number in num_common_hobbies_users],
            'users_sent_request_to': [user.to_user.username for user in users_sent_requests_to],
        })



@login_required
def friend_request_api(request):
    logged_in_user = request.user

    if request.method == "GET":
        requests = FriendRequest.objects.filter(to_user=logged_in_user)
        print(requests)
        arr = [request.from_user.to_dict() for request in requests]
        return JsonResponse({
            'data': arr
        })

    if request.method == "POST":
        try:
            POST = json.loads(request.body)
            to_user = POST["userToRequest"]
            friend_request = FriendRequest(
                from_user = logged_in_user,
                to_user = User.objects.get(username=to_user)
            )
            friend_request.save()
            return JsonResponse({})
        except:
            return HttpResponseNotFound("Invalid data")

    if request.method == "DELETE":
        try:
            POST = json.loads(request.body)
            to_user = POST["userToRemoveRequest"]
            friend_request = FriendRequest.objects.get(from_user=logged_in_user, to_user=User.objects.get(username=to_user))
            friend_request.delete()
            return JsonResponse({})
        except:
            return HttpResponseNotFound("Invalid data")

    return HttpResponseBadRequest("Invalid method")


@login_required
def remove_friend_api(request):

    body_unicode = request.body.decode('utf8')
    body = json.loads(body_unicode)

    if request.method == "DELETE":
        logged_in_user = get_object_or_404(User, username=request.user.username)
        friend_to_remove = User.objects.get(username=body['username'])
        logged_in_user.friends.remove(friend_to_remove)
        logged_in_user.save()
        return JsonResponse({})


@login_required
def friend_api(request):

    if request.method == "GET":
        logged_in_user = request.user.username
        users_friends_with = []
        num_common_hobbies_users = []
        for user in User.objects.all():
            if user.to_dict()["username"] == logged_in_user:
                continue
            else:
                friends_with_user = False
                for friend in user.friends.all():
                    if logged_in_user == friend.username:
                        friends_with_user = True
                        break
                if friends_with_user:
                    friend_hobbies = user.hobbies.all()
                    logged_in_user_hobbies = request.user.hobbies.all()

                    common_hobbies = list(set(friend_hobbies).intersection(logged_in_user_hobbies))
                    num_common_hobbies = len(common_hobbies)

                    users_friends_with.append(user)
                    num_common_hobbies_users.append(num_common_hobbies)

        return JsonResponse({
            'users_friends_with': [user.to_dict() for user in users_friends_with],
            'common_hobbies': [number for number in num_common_hobbies_users],
        })

    if request.method == "DELETE":
        logged_in_user = request.user
        try:
            POST = json.loads(request.body)
            friendToRemove = POST["friendToRemove"]
            logged_in_user.friends.remove(User.objects.get(username=friendToRemove))
            return JsonResponse({})
        except:
            return HttpResponseNotFound("Invalid data")

    return HttpResponseBadRequest("Invalid method")

@login_required
def acceptFriendRequest(request):
    logged_in_user = request.user
    user_object = get_object_or_404(User,username=logged_in_user.username)
    if request.method == "PUT":
        try:
            PUT = json.loads(request.body)
            friendToAdd = PUT["friendToAdd"]
            friend = User.objects.get(username=friendToAdd)
            FriendRequest.objects.filter(from_user=friend, to_user=request.user).delete()
            user_object.friends.add(friend)
            return JsonResponse({})
        except:
            return HttpResponseNotFound("Invalid data")

@login_required
def rejectFriendRequest(request):
    if request.method == "DELETE":
        DELETE = json.loads(request.body)
        friendToDelete = DELETE["friendToDelete"]
        result = User.objects.get(username=friendToDelete)
        FriendRequest.objects.filter(from_user=result, to_user=request.user).delete()
        return JsonResponse({})

    return HttpResponseBadRequest("Bad Request")

