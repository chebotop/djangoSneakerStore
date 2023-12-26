from django.contrib import admin
from django.utils.html import format_html
from .models import ShoeBrand, ShoeModel, ShoeGalleryImages, ShoeSize
from .forms import ShoeModelForm
import json


class ShoeModelAdmin(admin.ModelAdmin):
    form = ShoeModelForm
    list_display = ('image_tag', 'brand', 'model', 'price')

    @admin.display(description='Image')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" height="50" />', obj.image.url)
        return format_html('<span class="no-image">No Image</span>')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if request.FILES:
            for f in request.FILES.getlist('images'):  # 'images' - имя поля в форме
                ShoeGalleryImages.objects.create(shoe_model=obj, image=f)

    def render_change_form(self, request, context, *args, **kwargs):
        obj = kwargs.get('obj')
        if obj:
            image_urls_js = json.dumps([img.image.url for img in obj.shoe_gallery.all()])
            context['image_urls_js'] = image_urls_js
        return super().render_change_form(request, context, *args, **kwargs)


    class Media:
        js = ('js/image-upload.js',)


admin.site.register(ShoeBrand)
admin.site.register(ShoeModel, ShoeModelAdmin)
admin.site.register(ShoeSize)
admin.site.register(ShoeGalleryImages)