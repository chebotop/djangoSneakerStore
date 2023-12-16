from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ShoeBrand, ShoeModel, ShoeSize




class ShoeModelAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'model', 'brand', 'price')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'No Image'

    image_tag.short_description = 'Image'


admin.site.register(ShoeBrand)
admin.site.register(ShoeModel, ShoeModelAdmin)
admin.site.register(ShoeSize)
