from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("inventory", views.inventory, name="inventory"),
    path("computer/add", views.add_computer, name="add-computer"),
    path("computer/<int:computer_id>", views.update_computer, name="update-computer"),
    path("computer/<int:computer_id>/delete", views.delete_computer, name="delete-computer"),
    path("software", views.software, name="software"),
    path("software/add", views.add_software, name="add-software"),
    path("software/<int:software_id>", views.update_software, name="update-software"),
    path("software/<int:software_id>/delete", views.delete_software, name="delete-software"),
    path("login", views.user_login, name="login"),
    path("register", views.user_registration, name="register"),
    path("", RedirectView.as_view(pattern_name="inventory")) # Auto redirect index to inventory.
]