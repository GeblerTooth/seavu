from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inventory", views.inventory, name="inventory"),
    path("computer/add", views.add_computer, name="add-computer"),
    path("computer/<int:computer_id>", views.update_computer, name="update-computer"),
    path("computer/<int:computer_id>/delete", views.delete_computer, name="delete-computer"),
    path("software", views.software, name="software"),
    path("software/add", views.add_software, name="add-software"),
    path("software/<int:software_id>", views.update_software, name="update-software"),
    path("software/<int:software_id>/delete", views.delete_software, name="delete-software"),
    path("licences", views.licences, name="licences"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register")
]