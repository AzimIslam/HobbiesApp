from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import NullBooleanField
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(blank=True, null=True)
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
    requested_friends = models.ManyToManyField(
        to='self',
        blank=True,
        related_name="requests"
    )

    def to_dict(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'surname': self.last_name,
            'dob': self.date_of_birth,
            'city': self.city
        }

    def __str__(self):
        return self.username

    def get_hobbies(self):
        return [
            hobby.to_dict()
            for hobby in self.hobbies.all()
        ]


class Hobby(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_dict(self):
        return  {
            'name': self.name,
            'description': self.description,
            'api': reverse('hobby api', kwargs={'hobby_name': self.name}),
        }
