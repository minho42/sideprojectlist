from django.urls import path

from . import views

app_name = "project"


urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("tag=<str:tag>/", views.ProjectTagView.as_view(), name="tag"),
    path("submit/", views.ProjectCreateView.as_view(), name="submit"),
    path(
        "save-info-for-all/",
        views.ProjectCreateView.as_view(),
        name="save-info-for-all",
    ),
]
