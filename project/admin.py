from django.contrib import admin
from core.utils import get_all_fields

from .models import Project, Upvote


class ProjectAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Project)


class UpvoteAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Upvote)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Upvote, UpvoteAdmin)
