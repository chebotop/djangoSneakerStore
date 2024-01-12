from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('browse', views.catalog_page, name="catalog_page_all"),
    path('admin/', admin.site.urls),
    path('shoe/<int:shoe_id>', views.shoe_page),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity', views.update_quantity),
    path('checkout', views.checkout),
    path('checkout_process_guest', views.checkout_process_guest),
    path('confirmation', views.confirmation),
    path('browse/<str:brand_filter>/<str:category_filter>', views.catalog_page, name='catalog_page_filter'),
    path('browse/search_results', views.search_view, name='search_results')
]