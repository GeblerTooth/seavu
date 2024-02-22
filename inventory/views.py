from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.http import HttpResponse

from .forms import UserRegisterForm, EmployeeRegisterForm, ComputerForm
from .models import Computer

@login_required()
def index(request):
    return render(request, "inventory/index.html")

@login_required()
def inventory(request):
    computer_list = Computer.objects.all()
    return render(request, "inventory/inventory.html", {"computer_list": computer_list})

@login_required()
def delete_computer(request, computer_id):
    computer = Computer.objects.get(id=computer_id)
    computer.delete()
    return redirect('inventory')

@login_required()
def inspect_computer(request, computer_id):
    import sys
    computer = model_to_dict(Computer.objects.get(id=computer_id))
    print(str(computer), file=sys.stderr)
    return render(request, "inventory/inspect_computer.html", {"computer": computer})

@login_required()
def add_computer(request):
    if request.method == "POST":
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ComputerForm()
    return render(request, "inventory/add_computer.html", {"form": form})

@login_required()
def software(request):
    return HttpResponse("Hello from Software.")

@login_required()
def licences(request):
    return HttpResponse("Hello from Licences.")

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/')
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