from django.contrib import admin
from .models import Team
from django.utils.html import format_html

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src={object.photo.url} width="40px" style="border_radius:100px">')

    thumbnail.short_description = "photo"

    list_display = ("id", "thumbnail", "first_name", "designation", "is_best")
    list_display_links = ("id", "thumbnail", "first_name",)
    search_fields = ("first_name", "designation")
    list_filter = ("designation",)
    list_editable = ("is_best",)
    ordering = ("id",)

#Admin site Register
admin.site.register(Team, TeamAdmin)