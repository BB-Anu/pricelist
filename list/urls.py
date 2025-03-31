from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('import-excel/', import_excel, name='import_excel'),
    path('list-products/', list_products_view, name='list_products'),]