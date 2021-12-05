from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField()
    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
    )
    date_of_birth = models.DateField(null=True)
    hobbies = models.ManyToManyField('Hobby')
    email = models.EmailField()


class Country(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=2, unique=True)

class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )

class Hobby(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255)