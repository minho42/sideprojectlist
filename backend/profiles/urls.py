from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("<slug:slug>/edit/", views.update, name="update"),
    path("<slug:slug>/password/", views.change_password, name="change_password"),
    path("<slug:slug>/delete/", views.delete, name="delete"),
    path("<slug:slug>/", views.profile, name="user"),
]
