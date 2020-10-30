from django.contrib import admin

from core.utils import get_all_fields, get_all_fields_excluding

from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude_list = ["password", "slug"]
    list_display = get_all_fields_excluding(User, exclude_list)
    # list_display = get_all_fields(User)
    list_display_links = ["username", "first_name", "last_name"]
    # filter_horizontal = [""]


admin.site.register(User, UserAdmin)
