from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student

# # Register your models here.
class CustomerUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser, CustomerUserAdmin)
admin.site.register(Student,)