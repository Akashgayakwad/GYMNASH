from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CredUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CredUser
        fields = ('first_name','last_name','contact','aadhar','gymowner')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CredUser
        fields = ('first_name','last_name','password','contact','gymowner')