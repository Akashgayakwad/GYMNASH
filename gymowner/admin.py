from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import CredUser,GYM

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CredUser
    UserAdmin.add_fieldsets += (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','contact','aadhar','gymowner')}
        ),
    )
    UserAdmin.fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','contact','aadhar','gymowner')}
        ),
    )
    list_display = ('first_name','last_name','gymowner')

admin.site.register(CredUser, CustomUserAdmin)

admin.site.register(GYM)