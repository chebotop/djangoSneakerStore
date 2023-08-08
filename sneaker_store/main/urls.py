from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sheets_bot/', views.sheets_bot, name='sheets_bot')
]