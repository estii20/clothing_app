from django.urls import path
from . import views
from .views import create_clothing_item


urlpatterns = [
    path('add/', create_clothing_item, name='create_clothing_item'),  
    path('', views.item_list, name='item_list'),
    path('clothing/<int:item_id>/', views.item_detail, name='item_detail'),
]
