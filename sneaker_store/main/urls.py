from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sheets_bot/', views.sheets_bot, name='sheets_bot'),
    path('catalog/', views.catalog, name='catalog'),  # Список всех товаров
    path('catalog/<int:product_id>/', views.product_detail, name='product_detail'),  # Детали конкретного товара
    path('catalog/category/<int:category_id>/', views.category, name='category_detail'),  # Список товаров определенной категории
]