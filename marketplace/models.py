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

    AGE_GROUP_CHOICES = [
        ('baby', 'Baby (0-24m)'),
        ('toddler', 'Toddler (2-4y)'),
        ('kids', 'Kids (4-7y)'),
        ('big_kids', 'Big Kids (8-12y)'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    size = models.CharField(max_length=20)
    image = models.ImageField(upload_to='clothing_images/')
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES, default='kids')
    is_featured = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClothingImage(models.Model):
    item = models.ForeignKey('ClothingItem', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='clothing_images/extra/')

    def __str__(self):
        return f"Image for {self.item.title}"
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.full_name}, {self.address_line1}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price
    

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"