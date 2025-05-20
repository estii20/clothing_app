# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_clothing_item, name='add_clothing_item'),
]
