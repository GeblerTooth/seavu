import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import UserRegisterForm, AuthenticationForm, EmployeeRegisterForm, ComputerForm, SoftwareForm
from .models import Computer, Software

logger = logging.getLogger(__name__)

def verbose_user(request) -> str:
    """Returns a unique string representing the user within the request. Meant for logging purposes."""
    return f"{request.user.pk}:{request.user.username}"

@login_required()
@require_http_methods(['GET', 'POST'])
def add_computer(request):
    """Django view for creating a Computer model."""
    if request.method == "POST":
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"{verbose_user(request)} sucessfully added Computer {form.cleaned_data.get('name')}.")
            messages.success(request, f"{request.POST.get('name')} was added successfully.")
            return redirect('inventory')
    else:
        form = ComputerForm()
    return render(request, "inventory/add_computer.html", {"form": form})

@login_required()
@require_http_methods(['GET'])
def inventory(request):
    """Django view for viewing all Computer models."""
    computer_list = Computer.objects.all()
    return render(request, "inventory/inventory.html", {"computer_list": computer_list})

@login_required()
@require_http_methods(['GET', 'POST'])
def update_computer(request, computer_id):
    """Django view for updating a Computer model."""
    computer = get_object_or_404(Computer, id=computer_id)
    if request.method == "POST":
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            logger.info(f"{verbose_user(request)} sucessfully updated Computer {form.cleaned_data.get('name')}.")
            messages.success(request, f"{request.POST.get('name')} was updated successfully.")
    else:
        form = ComputerForm(instance=computer)
    return render(request, "inventory/update_computer.html", {"form": form})

@staff_member_required()
@require_http_methods(['POST'])
def delete_computer(request, computer_id):
    """Django view for deleting a Computer model."""
    computer = Computer.objects.get(id=computer_id)
    computer.delete()
    logger.info(f"{verbose_user(request)} sucessfully deleted Computer {computer}.")
    messages.success(request, f"{computer} was deleted successfully.")
    return redirect('inventory')

@login_required()
@require_http_methods(['GET', 'POST'])
def add_software(request):
    """Django view for creating a Software model."""
    if request.method == "POST":
        form = SoftwareForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"{verbose_user(request)} sucessfully added Software {form.cleaned_data.get('name')}.")
            messages.success(request, f"{request.POST.get('name')} was added successfully.")
            return redirect('software')
    else:
        form = SoftwareForm()
    return render(request, "inventory/add_software.html", {"form": form})

@login_required()
@require_http_methods(['GET'])
def software(request):
    """Django view for viewing all Software models."""
    software_list = Software.objects.all()
    return render(request, "inventory/software.html", {"software_list": software_list})

@login_required()
@require_http_methods(['GET', 'POST'])
def update_software(request, software_id):
    """Django view for updating a Software model."""
    software = get_object_or_404(Software, id=software_id)
    if request.method == "POST":
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            form.save()
            logger.info(f"{verbose_user(request)} sucessfully updated Software {form.cleaned_data.get('name')}.")
            messages.success(request, f"{request.POST.get('name')} was updated successfully.")
    else:
        form = SoftwareForm(instance=software)
    return render(request, "inventory/update_software.html", {"form": form})

@staff_member_required()
@require_http_methods(['POST'])
def delete_software(request, software_id):
    """Django view for deleting a Software model."""
    software = Software.objects.get(id=software_id)
    software.delete()
    logger.info(f"{verbose_user(request)} sucessfully deleted Software {software}.")
    messages.success(request, f"{software} was deleted successfully.")
    return redirect('software')

@require_http_methods(['GET', 'POST'])
def user_login(request):
    """Django view for logging a User in."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                logger.info(f"{verbose_user(request)} sucessfully logged in.")
                messages.info(request, f"Welcome {user}.")
                return redirect('inventory')
        logger.info(f"Failed login attempt for {form.cleaned_data.get('username')}.")
    elif request.user.is_authenticated:
        return redirect('inventory')
    else:
        form = AuthenticationForm(request)
    return render(request, "registration/login.html", {"form": form})

@require_http_methods(['GET', 'POST'])
def user_registration(request):
    """Django view for registering a User (and Employee)."""
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        employee_form = EmployeeRegisterForm(request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user_instance = user_form.save(commit=False) # Get user instance by saving a non-commit.
            employee_form.instance.user = user_instance # Set user instance as employee foreign key.
            user_form.save()
            employee_form.save()
            logger.info(f"{user_instance.pk}:{user_instance.username} sucessfully registered.")
            messages.success(request, f"Sucessfully registered.")
            # Automatically login user if possible.
            user = authenticate(request, username=user_form.cleaned_data.get('username'), password=user_form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome {user}.")
                return redirect('inventory')
            else:
                return redirect('login')
        logger.info(f"Failed login attempt for {user_form.cleaned_data.get('username')}.")
    else:
        user_form = UserRegisterForm()
        employee_form = EmployeeRegisterForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'employee_form': employee_form})