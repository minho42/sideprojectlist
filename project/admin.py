from django.contrib import admin
from core.utils import get_all_fields

from .models import Project, Like


class ProjectAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Project)
    list_display_links = ["slug", "link", "maker_fullname"]


class LikeAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Like)
    list_display_links = ["project", "user"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Like, LikeAdmin)