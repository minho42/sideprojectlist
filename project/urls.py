from django.urls import path

from . import views

app_name = "project"


urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("add/", views.ProjectCreateView.as_view(), name="add"),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="detail"),
    # path("<slug:slug>/edit/", views.ProjectUpdateView.as_view(), name="update"),
    # path("<slug:slug>/delete/", views.ProjectDeleteView.as_view(), name="delete"),
]
