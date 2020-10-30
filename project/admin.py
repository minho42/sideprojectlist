from django.contrib import admin
from core.utils import get_all_fields

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Project)


admin.site.register(Project, ProjectAdmin)
