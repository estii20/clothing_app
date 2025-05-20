from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import ClothingItem
from .forms import ClothingItemForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Optional: for user feedback

@login_required
def add_clothing_item(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.seller = request.user
            clothing_item.save()
            messages.success(request, 'Clothing item added successfully!')  # Optional
            return redirect('item_list')  # Ensure this view exists
    else:
        form = ClothingItemForm()
    return render(request, 'store/add_clothing_item.html', {'form': form})


def item_list(request):
    items = ClothingItem.objects.all().order_by('-created_at')
    return render(request, 'marketplace/item_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(ClothingItem, pk=pk)
    return render(request, 'marketplace/item_detail.html', {'item': item})