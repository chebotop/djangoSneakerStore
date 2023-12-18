from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ShoeBrand, ShoeModel, ShoeGalleryImages, ShoeSize
from .forms import ShoeModelForm


# class ShoeImageInline(admin.TabularInline):  # Или admin.StackedInline
#     model = ShoeImage
#     extra = 5


class ShoeModelAdmin(admin.ModelAdmin):
    form = ShoeModelForm
    list_display = ('image_tag', 'model', 'brand', 'price')

    def image_tag(self, obj):
        # Демонстрация первого изображения из связанных изображений
        images = obj.images.all()
        if images:
            return mark_safe(f'<img src="{images[0].image.url}" width="50" height="50" />')
        return 'No Image'
    image_tag.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if request.FILES:
            for f in request.FILES.getlist('images'):  # 'images' - имя поля в форме
                ShoeGalleryImages.objects.create(shoe_model=obj, image=f)


    class Media:
        js = ('js/image-upload.js',)

admin.site.register(ShoeBrand)
admin.site.register(ShoeModel, ShoeModelAdmin)
admin.site.register(ShoeSize)
admin.site.register(ShoeGalleryImages)



