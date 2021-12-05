from django.contrib import admin
from .models import User, Hobby, City

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "date_of_birth"]

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


admin.site.register(City)
