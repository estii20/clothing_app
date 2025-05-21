from django.contrib import admin
from .models import ClothingItem, ClothingImage

class ClothingImageInline(admin.TabularInline):
    model = ClothingImage
    extra = 1

@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    inlines = [ClothingImageInline]
    list_display = (
        'title',
        'seller',
        'category',
        'condition',
        'size',
        'price',
        'is_featured',
        'created_at',
    )
    list_filter = ('category', 'condition', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

