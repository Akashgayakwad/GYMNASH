from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CredUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CredUser
        fields = ('first_name','last_name','contact','aadhar','gymowner')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CredUser
        password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
        fields = ('first_name','last_name','password','contact','gymowner')