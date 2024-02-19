from django.db import models
from django.contrib.auth.models import User

from datetime import date

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.PositiveSmallIntegerField(choices={0: "Full", 1: "Part", 2: "Contractor", 3: "Volunteer", 4: "Other"}, blank=True, null=True)
    department = models.CharField(max_length=128, blank=True, null=True)

class Computer(models.Model):
    name = models.CharField(max_length=15, help_text="System name or other.") # Max Length for Windows System Name is 15 chars.
    status = models.PositiveSmallIntegerField(choices={0: "Active", 1: "Inactive", 2: "Awaiting return", 3: "In transit", 4: "Awaiting repairs", 5: "Lost", 6: "Stolen", 7: "Quarantined", 8: "Unknown"})
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    serial_number = models.CharField(max_length=128, blank=True, null=True)
    tag_number = models.CharField(max_length=128, blank=True, null=True)
    category = models.PositiveSmallIntegerField(choices={0: "PC", 1: "Laptop", 2: "Mini PC", 3: "SBC", 4: "All-in-One PC", 5: "Server", 6: "NAS", 7: "Other"})
    date_of_purchase = models.DateField(default=date.today, blank=True, null=True)
    memory_gb = models.PositiveIntegerField(blank=True, null=True)
    storage_gb = models.PositiveIntegerField(blank=True, null=True)
    cores = models.PositiveSmallIntegerField(blank=True, null=True)
    clock_speed_ghz = models.FloatField(blank=True, null=True)
    gpu = models.CharField(max_length=256, blank=True, null=True)

class Software(models.Model):
    name = models.CharField(max_length=256)
    company_requisite = models.BooleanField()
    has_license = models.BooleanField()

class ComputerSoftware(models.Model): # Join table for Computer and Software.
    computer_id = models.ForeignKey("Computer", on_delete=models.CASCADE)
    software_id = models.ForeignKey("Software", on_delete=models.CASCADE)