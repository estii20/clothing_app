from django import forms
from .models import ClothingItem

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = [
            'title', 'description', 'price',
            'category', 'condition', 'size',
            'image', 'is_featured'
        ]
