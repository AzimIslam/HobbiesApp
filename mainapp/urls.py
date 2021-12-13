"""mainapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views, api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Root URL
    #path('', views.index, name='Movies and Actors'),

    path('', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('home/', views.home_view, name="home"),
    path('logout/', views.logout, name="logout"),
    path('createHobbies/', views.create_hobbies_view, name="createHobbies"),
    path('searchHobbies/', views.search_hobbies_view, name="searchHobbies"),
    path('social/', views.social_view, name="social"),
    path('friends/', views.friends_view, name="friends"),
    path('pendingFriendRequests/', views.pending_friend_request_view, name="pendingFriendRequests"),
    path('profile/<str:username>', views.user_profile_view, name="userProfile"),

    path('api/hobbies/', api.hobbies_api, name="hobbies api"),
    path('api/toggleHobby/', api.toggle_hobby, name="toggle hobby api"),
    path('api/userHobbies/', api.user_hobbies_api, name="user hobbies api"),
    path('api/createHobby/', api.hobbie_api, name="hobbie api"), # createHobby api
    path('api/profile/', api.profile_api, name="profile api"),
    path('api/hobby/<str:hobby_name>/', api.hobby_api, name="hobby api"),
    path('api/deleteUserHobby/', api.user_delete_hobby, name="delete hobby api"),
    path('api/uploadFile/', api.uploadFiles, name="uploadFile api"),
    path('api/users/', api.users_api, name="users api"),
    path('api/friendRequest/', api.friend_request_api, name="friend request api"),
    path('api/friend/', api.friend_api, name="friend api"),
    path("api/acceptFriendRequest/", api.acceptFriendRequest, name="accept friend request"),
    path("api/rejectFriendRequest/", api.rejectFriendRequest, name="reject friend request")


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
