from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import NullBooleanField
from django.urls import reverse
import datetime

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(default="default.png" ,blank=True, null=True)
    city = models.CharField(blank=True, max_length=150, null=True)
    date_of_birth = models.DateField(null=True)
    hobbies = models.ManyToManyField(
        'Hobby',
        blank=True
    )
    email = models.EmailField()
    friends = models.ManyToManyField(
        to='self',
        blank=True,
        related_name='friends'
    )

    def to_dict(self):
        today = datetime.date.today()
        dob = self.date_of_birth
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        
        return {
            'username': self.username,
            'profile_pic': self.get_profile_picture(),
            'first_name': self.first_name,
            'surname': self.last_name,
            'dob': self.date_of_birth,
            'age': age,
            'city': self.city,
            'email': self.email,
            'profile': reverse('user profile api', kwargs={'username': self.username}),
            'hobbies': self.get_hobbies(),
        }

    def get_profile_picture(self):
        if self.profile_pic:
            return self.profile_pic.url
        else:
            return "/assets/images/default.png"


    def __str__(self):
        return self.username

    def get_hobbies(self):
        return [
            hobby.to_dict()
            for hobby in self.hobbies.all()
        ]

class FriendRequest(models.Model): 
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")



class Hobby(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def to_dict(self):
        return  {
            'name': self.name,
            'description': self.description,
            'api': reverse('hobby api', kwargs={'hobby_name': self.name}),
        }
