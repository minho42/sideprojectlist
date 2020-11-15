from django.contrib import admin
from core.utils import get_all_fields

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Project)
    list_display_links = ["slug", "link", "maker_fullname"]


admin.site.register(Project, ProjectAdmin)
