from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hobby, Country, City

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Hobby)
admin.site.register(Country)
admin.site.register(City)