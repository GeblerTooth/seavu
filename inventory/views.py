from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict

from .forms import UserRegisterForm, EmployeeRegisterForm, ComputerForm, SoftwareForm
from .models import Computer, Software

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
def update_computer(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    if request.method == "POST":
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
    else:
        form = ComputerForm(instance=computer)
    return render(request, "inventory/update_computer.html", {"form": form})

@login_required()
def add_computer(request):
    if request.method == "POST":
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ComputerForm()
    return render(request, "inventory/add_computer.html", {"form": form})

@login_required()
def software(request):
    software_list = Software.objects.all()
    return render(request, "inventory/software.html", {"software_list": software_list})

@login_required()
def delete_software(request, software_id):
    software = Software.objects.get(id=software_id)
    software.delete()
    return redirect('software')

@login_required()
def update_software(request, software_id):
    software = get_object_or_404(Software, id=software_id)
    if request.method == "POST":
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            form.save()
    else:
        form = SoftwareForm(instance=software)
    return render(request, "inventory/update_software.html", {"form": form})

@login_required()
def add_software(request):
    if request.method == "POST":
        form = SoftwareForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('software')
    else:
        form = SoftwareForm()
    return render(request, "inventory/add_software.html", {"form": form})

@login_required()
def licences(request):
     return render(request, "inventory/licences.html")

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
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        employee_form = EmployeeRegisterForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'employee_form': employee_form})