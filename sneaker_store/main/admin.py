from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
<<<<<<< HEAD
from .models import ShoeBrand, ShoeModel, ShoeSize

=======
from .models import ShoeBrand, ShoeModel, ShoeImage, ShoeSize
from .forms import ShoeModelForm
>>>>>>> 399bc5d090769e750f9502be8a936b2f2f60f4c3


class ImageAdmin(admin.StackedInline):
    model = ShoeImage

class ShoeModelAdmin(admin.ModelAdmin):
    form = ShoeModelForm  # Использование кастомной формы
    list_display = ('image_tag', 'model', 'brand', 'price')
    inlines = [ImageAdmin]

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'No Image'

    image_tag.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if 'extra_images' in form.cleaned_data:
            for f in request.FILES.getlist('extra_images'):
                ShoeImage.objects.create(shoe_model=obj, image=f)


admin.site.register(ShoeBrand)
admin.site.register(ShoeModel, ShoeModelAdmin)
admin.site.register(ShoeSize)
<<<<<<< HEAD
=======
admin.site.register(ShoeImage)
>>>>>>> 399bc5d090769e750f9502be8a936b2f2f60f4c3
