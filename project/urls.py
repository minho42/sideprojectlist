from django.urls import path

from . import views

app_name = "project"


urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("add/", views.ProjectCreateView.as_view(), name="add"),
    path(
        "save-info-for-all/",
        views.ProjectCreateView.as_view(),
        name="save-info-for-all",
    ),
]
