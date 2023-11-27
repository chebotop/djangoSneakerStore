from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('browse', views.catalog_page, name="catalog_page_all"),
    path('admin/', admin.site.urls),
    # path('admin/add_shoe_page', views.add_shoe_page),
    # path('admin/add_shoe', views.add_shoe),
    # path('admin/shoe_list', views.shoe_list),
    # path('admin/update_desc', views.update_desc),
    # path('admin/update_img', views.update_img),
    # path('admin/update_price', views.update_price),
    path('shoe/<int:shoe_id>', views.shoe_page),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity', views.update_quantity),
    path('checkout', views.checkout),
    path('checkout_process_guest', views.checkout_process_guest),
    path('confirmation', views.confirmation),
    path('admin/orders', views.orders_page),
    path('admin/update_status', views.update_status),
    path('admin/order/<int:order_id>', views.order_details),
    path('admin', views.admin_menu),
    path('admin/login', views.admin_login),
    path('admin/logout', views.admin_logout),
    path('browse/<str:browse_filter>', views.catalog_page, name='catalog_page_filter'),

]