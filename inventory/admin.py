from django.contrib import admin

from .models import Employee, Computer, Software, ComputerSoftware

admin.site.register({Employee, Computer, Software, ComputerSoftware})