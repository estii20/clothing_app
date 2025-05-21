from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import ClothingItem, ClothingImage
from .forms import ClothingItemForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  


@login_required
def create_clothing_item(request):
    if request.method == 'POST':
        item_form = ClothingItemForm(request.POST, request.FILES)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.seller = request.user
            item.save()

            # Handle multiple images uploaded from the 'images' input field (see template below)
            for img in request.FILES.getlist('images'):
                ClothingImage.objects.create(item=item, image=img)

            return redirect('item_detail', pk=item.pk)
    else:
        item_form = ClothingItemForm()

    return render(request, 'marketplace/create_clothing_item.html', {
        'item_form': item_form,
    })




def item_list(request):
    items = ClothingItem.objects.all().order_by('-created_at')
    return render(request, 'marketplace/item_list.html', {'items': items})


def item_detail(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id)

    # Filter similar items
    similar_items = ClothingItem.objects.filter(
        category=item.category,
        size=item.size
    ).exclude(id=item.id)[:4]  

    return render(request, 'marketplace/item_detail.html', {
        'item': item,
        'related_items': similar_items
    })