from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Computer, Software

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class EmployeeRegisterForm(forms.ModelForm):

    class Meta:
        model = Employee
        exclude = ('user',) # Exclude user OneToOneField.

class ComputerForm(forms.ModelForm):
    
    class Meta:
        model = Computer
        fields = '__all__'

class SoftwareForm(forms.ModelForm):
    
    class Meta:
        model = Software
        fields = '__all__'