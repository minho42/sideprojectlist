from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views.generic import (
    CreateView,
    ListView,
)

# from .forms import DistrictCreateForm, DistrictPasswordChangeForm, DistrictUpdateForm
from .models import Project


class ProjectTagView(ListView):
    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(is_approved=True).filter(tags__icontains=self.kwargs["tag"]).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_selected"] = self.kwargs["tag"]
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "project/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(is_approved=True).order_by("-created")


class ProjectCreateView(CreateView):
    model = Project
    fields = [
        "link",
        "maker_fullname",
        "twitter_handle",
        "github_handle",
        "tags",
    ]
    # form_class = ProjectCreateForm
    template_name = "project/project_create.html"

    # def form_valid(self, form):
    #     form.instance.submitted_by = self.request.user
    #     try:
    #         success_url = super().form_valid(form)
    #         form.instance.save()
    #         return success_url
    #     except IntegrityError as e:
    #         # TODO
    #         messages.error(self.request, f"Something went wrong: {e}")
    #         return HttpResponseRedirect(reverse("project:submit"))
