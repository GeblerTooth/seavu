from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages

from .forms import UserRegisterForm, EmployeeRegisterForm
from .models import Computer

@login_required()
def index(request):
    computer_list = Computer.objects.all()
    return render(request, "inventory/index.html", {"computer_list": computer_list})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect.")
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        employee_form = EmployeeRegisterForm(request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            # Automatically asign the user to the employee.
            user_instance = user_form.save(commit=False) # Get user instance by saving a non-commit.
            employee_form.instance.user = user_instance # Set user instance as employee foreign key.
            user_form.save()
            employee_form.save()
    else:
        user_form = UserRegisterForm()
        employee_form = EmployeeRegisterForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'employee_form': employee_form})