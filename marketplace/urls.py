from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_clothing_item, name='add_clothing_item'),
    path('', views.item_list, name='item_list'),
]
