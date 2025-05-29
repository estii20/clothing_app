from django.urls import path
from . import views
from .views import create_clothing_item


urlpatterns = [
    path('add/', create_clothing_item, name='create_clothing_item'),  
    path('', views.item_list, name='item_list'),
    path('clothing/<int:item_id>/', views.item_detail, name='item_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('shipping-address/', views.add_shipping_address, name='add_shipping_address'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:item_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('about/', views.about_view, name='about'),
    path('shipping/', views.shipping_view, name='shipping'),
    path('returns/', views.returns_view, name='returns'),
    path('contact/', views.contact_view, name='contact'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('search/', views.search_view, name='search'),
]
