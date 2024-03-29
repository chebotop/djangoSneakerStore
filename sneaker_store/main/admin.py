from django.contrib import admin
from django.utils.html import format_html
from .models import ShoeBrand, ShoeModel, ShoeGalleryImages, CategoryModel, ShoeSize
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase
from .forms import ShoeModelForm, CategoryModelForm, ShoeBrandForm
from mptt.admin import MPTTModelAdmin


class ShoeGalleryImagesInline(SortableInlineAdminMixin, admin.StackedInline):  # Или admin.StackedInline
    model = ShoeGalleryImages
    extra = 1  # Количество форм для новых записей
    fields = ('image', 'image_tag',)  # поля для отображения
    readonly_fields = ('image_tag',)

    @admin.display(description='Изображение')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" height="50" />', obj.image.url)
        return format_html('<span class="no-image">No Image</span>')


class ShoeBrandAdmin(SortableAdminBase, MPTTModelAdmin, admin.ModelAdmin):
    list_display = ('brand', )


class ShoeModelAdmin(SortableAdminBase, MPTTModelAdmin, admin.ModelAdmin):
    form = ShoeModelForm
    list_display = ('image_tag', 'brand', 'parent', 'price')
    inlines = [ShoeGalleryImagesInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        brand_id = request.GET.get('brand_id')
        category_id = request.GET.get('category_id')
        if brand_id and category_id:
            form.base_fields['brand'].initial = brand_id
            form.base_fields['parent'].initial = category_id
        return form

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


class CategoryModelAdmin(SortableAdminBase, MPTTModelAdmin, admin.ModelAdmin):
    form = CategoryModelForm
    list_display = ['name', 'parent']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        brand_id = request.GET.get('brand_id')
        if brand_id:
            form.base_fields['parent'].initial = brand_id
        return form


class ShoeBrandAdmin(MPTTModelAdmin):
    form = ShoeBrandForm
    list_display = ['image_tag', 'name']

    @admin.display(description='Thumbnail')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="55" height="45" />', obj.image.url)
        return format_html('<span class="no-image">No Image</span>')


admin.site.register(ShoeBrand, ShoeBrandAdmin)
admin.site.register(CategoryModel, CategoryModelAdmin)
admin.site.register(ShoeModel, ShoeModelAdmin)

# admin.site.register(ShoeSize)
# Не удалять, пока существует данная модель в базе данных
# @admin.register(ShoeGalleryImages)
# class ShoeGalleryImagesAdmin(SortableAdminMixin, admin.ModelAdmin):
#     pass