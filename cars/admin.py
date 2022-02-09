from django.contrib import admin
from .models import Car
from django.utils.html import format_html

class CarAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src={object.car_photo1.url} width="40px" style="border_radius:100px">')

    thumbnail.short_description = "photo"

    list_display = ("id", "thumbnail", "car_title", "state", "body_style", "fuel_type", "is_featured")
    list_display_links = ("id", "thumbnail", "car_title",)
    search_fields = ("car_title", "body_style")
    list_filter = ("body_style","fuel_type",)
    list_editable = ("is_featured",)
    ordering = ('-id',)
admin.site.register(Car, CarAdmin)