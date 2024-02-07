from django.shortcuts import render

from .models import Computer

def index(request):
    computer_list = Computer.objects.all()
    return render(request, "inventory/index.html", {"computer_list": computer_list})