from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inventory", views.inventory, name="inventory"),
    path("inventory/computer/add", views.add_computer, name="add-computer"),
    path("inventory/computer/<int:computer_id>", views.inspect_computer, name="inspect-computer"),
    path("inventory/computer/<int:computer_id>/delete", views.delete_computer, name="delete-computer"),
    path("software", views.software, name="software"),
    path("licences", views.licences, name="licences"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register")
]