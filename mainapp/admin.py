from django.contrib import admin
from .models import User, Hobby, City

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "date_of_birth"]

admin.site.register(Hobby)
admin.site.register(City)