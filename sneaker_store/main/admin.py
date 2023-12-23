from django.contrib import admin
from django.utils.html import format_html
from .models import ShoeBrand, ShoeModel, ShoeGalleryImages, ShoeSize
from .forms import ShoeModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple


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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "images":
            kwargs["widget"] = FilteredSelectMultiple(is_stacked=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['images'].initial = obj.images.order_by('your_order_field')
        return form

    class Media:
        js = ('js/image-upload.js',)


admin.site.register(ShoeBrand)
admin.site.register(ShoeModel, ShoeModelAdmin)
admin.site.register(ShoeSize)
admin.site.register(ShoeGalleryImages)



