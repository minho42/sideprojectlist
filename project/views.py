from django.utils.html import format_html
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# from .forms import DistrictCreateForm, DistrictPasswordChangeForm, DistrictUpdateForm
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(is_approved=True).order_by("-created")


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = [
        "link",
        "maker_fullname",
        "twitter_handle",
        "github_handle",
        "producthunt_handle",
    ]
    # form_class = ProjectCreateForm
    template_name = "project/project_create.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "project/project_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(slug=self.kwargs["slug"])
        return qs
