from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(blank=True)
    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
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

    def __str__(self):
        return self.username


class City(models.Model):
    name = models.CharField(max_length=150)

class Hobby(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255)