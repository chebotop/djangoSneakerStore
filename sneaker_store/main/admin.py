from django.contrib import admin
from .models import Category, Product, SubCategory

admin.site.site_header = "Crossboost admin panel"
admin.site.site_title = "Crossboost"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # здесь можно указать поля, которые вы хотите видеть в списке категорий
    search_fields = ('name',)  # поиск по имени категории

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # поля, которые будут отображаться в списке подкатегорий
    search_fields = ('name',)  # поля, по которым можно будет искать
    list_filter = ('category',)  # фильтры для быстрого поиска подкатегорий по категориям

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # поля, которые будут отображаться в списке товаров
    search_fields = ('name',)  # поля, по которым можно будет искать
    list_filter = ('price',)  # фильтры для быстрого поиска товаров по определенным критериям
