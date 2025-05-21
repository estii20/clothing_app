from django.db import models
from django.contrib.auth.models import User

class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('Tops', 'Tops'),
        ('Bottoms', 'Bottoms'),
        ('Shoes', 'Shoes'),
        ('Outerwear', 'Outerwear'),
        ('Accessories', 'Accessories'),
    ]

    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Used', 'Used'),
        ('Well Loved', 'Well Loved'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    size = models.CharField(max_length=20)
    image = models.ImageField(upload_to='clothing_images/')
    is_featured = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClothingImage(models.Model):
    item = models.ForeignKey('ClothingItem', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='clothing_images/extra/')

    def __str__(self):
        return f"Image for {self.item.title}"