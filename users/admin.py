from django.contrib import admin
from django.utils.html import format_html
from .models import Distances, Locations, LocationImage

admin.site.register(Locations)

# Register your models here.

@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'location_id']
    search_fields = ['location_id', 'image']
    list_filter = ['location_id']
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:auto;" />', obj.image.url)
        return "-"
    image_thumbnail.short_description = 'Thumbnail'