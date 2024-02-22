from django.db import models
from django.contrib.auth.models import User

from datetime import date

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=128, choices={"Full": "Full", "Part": "Part", "Contractor": "Contractor", "Volunteer": "Volunteer", "Other": "Other"}, blank=True, null=True)
    department = models.CharField(max_length=128, blank=True, null=True)

class Computer(models.Model):
    name = models.CharField(max_length=15, help_text="System name or other.") # Max Length for Windows System Name is 15 chars.
    status = models.CharField(max_length=128, choices={"Active": "Active", "Inactive": "Inactive", "Awaiting return": "Awaiting return", "In transit": "In transit", "Awaiting repairs": "Awaiting repairs", "Lost": "Lost", "Stolen": "Stolen", "Quarantined": "Quarantined", "Unknown": "Unknown"})
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    serial_number = models.CharField(max_length=128, blank=True, null=True)
    tag_number = models.CharField(max_length=128, blank=True, null=True)
    category = models.CharField(max_length=128, choices={"PC": "PC", "Laptop": "Laptop", "Mini PC": "Mini PC", "SBC": "SBC", "All-in-One PC": "All-in-One PC", "Server": "Server", "NAS": "NAS", "Other": "Other"})
    date_of_purchase = models.DateField(default=date.today, blank=True, null=True)
    memory_gb = models.PositiveIntegerField(blank=True, null=True)
    storage_gb = models.PositiveIntegerField(blank=True, null=True)
    cores = models.PositiveSmallIntegerField(blank=True, null=True)
    clock_speed_ghz = models.FloatField(blank=True, null=True)
    gpu = models.CharField(max_length=256, blank=True, null=True)

class Software(models.Model):
    name = models.CharField(max_length=256)
    company_requisite = models.BooleanField()
    has_licence = models.BooleanField()

class ComputerSoftware(models.Model): # Join table for Computer and Software.
    computer_id = models.ForeignKey("Computer", on_delete=models.CASCADE)
    software_id = models.ForeignKey("Software", on_delete=models.CASCADE)