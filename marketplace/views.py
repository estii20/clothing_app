from django.shortcuts import render, redirect
from .forms import ClothingItemForm
from django.contrib.auth.decorators import login_required

@login_required
def add_clothing_item(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.seller = request.user  # Assign current user as seller
            clothing_item.save()
            return redirect('home')  # Change to your actual redirect target
    else:
        form = ClothingItemForm()
    return render(request, 'store/add_clothing_item.html', {'form': form})

