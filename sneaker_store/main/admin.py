from django.contrib import admin
from django.utils.html import format_html
from .models import ShoeBrand, ShoeModel, ShoeGalleryImages, CategoryModel
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase
from .forms import ShoeModelForm
from mptt.admin import MPTTModelAdmin

class ShoeGalleryImagesInline(SortableInlineAdminMixin, admin.StackedInline):  # Или admin.StackedInline
    model = ShoeGalleryImages
    extra = 1  # Количество форм для новых записей
    fields = ('image', 'image_tag',)  # поля для отображения
    readonly_fields = ('image_tag',)

    @admin.display(description='Image')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" height="50" />', obj.image.url)
        return format_html('<span class="no-image">No Image</span>')


class ShoeModelAdmin(SortableAdminBase, MPTTModelAdmin, admin.ModelAdmin):
    form = ShoeModelForm
    list_display = ('image_tag', 'brand', 'model', 'price')
    inlines = [ShoeGalleryImagesInline]

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

    class Media:
        js = ('js/image-upload.js',)

# Не удалять, пока существует данная модель в базе данных
# @admin.register(ShoeGalleryImages)
# class ShoeGalleryImagesAdmin(SortableAdminMixin, admin.ModelAdmin):
#     pass


admin.site.register(ShoeBrand, MPTTModelAdmin)
admin.site.register(CategoryModel, MPTTModelAdmin)
admin.site.register(ShoeModel, ShoeModelAdmin)

# admin.site.register(ShoeSize)
