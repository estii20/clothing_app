from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .models import ClothingItem, ClothingImage
from .forms import ClothingItemForm, CustomLoginForm, CustomSignupForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


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


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'


def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('item_list')
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, item_data in cart.items():
        item = get_object_or_404(ClothingItem, id=item_id)
        quantity = item_data['quantity']
        item_total = item.price * quantity
        cart_items.append({
            'id': item.id,
            'title': item.title,
            'image': item.image,
            'size': item.size,
            'price': item.price,
            'quantity': quantity,
            'total_price': item_total,
        })
        total += item_total

    return render(request, 'marketplace/cart.html', {
        'cart_items': cart_items,
        'cart_total': total,
    })


@require_POST
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    cart[item_id] = {'quantity': cart.get(item_id, {}).get('quantity', 0) + 1}
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return redirect('cart')


@require_POST
def update_cart_quantity(request, item_id):
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if item_id in cart:
        if action == 'increase':
            cart[item_id]['quantity'] += 1
        elif action == 'decrease':
            cart[item_id]['quantity'] = max(1, cart[item_id]['quantity'] - 1)
        request.session['cart'] = cart

    return redirect('cart')


@require_POST
def process_payment(request):
    # Simulate payment processing...
    request.session['cart'] = {}  # Clear the cart
    return redirect('order_confirmation')  # Name this URL in your urls.py


def order_confirmation(request):
    return render(request, 'marketplace/order_confirmation.html')


@require_POST
def process_payment(request):
    try:
        data = json.loads(request.body)
        if data.get('confirm'):
            request.session['cart'] = {}
            return JsonResponse({'status': 'ok'})
    except Exception:
        pass
    return JsonResponse({'status': 'error'}, status=400)