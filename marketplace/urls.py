from django.urls import path
from . import views
from .views import create_clothing_item, cart_view


urlpatterns = [
    path('add/', create_clothing_item, name='create_clothing_item'),  
    path('', views.item_list, name='item_list'),
    path('clothing/<int:item_id>/', views.item_detail, name='item_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
]
