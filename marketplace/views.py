from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .models import ClothingItem, ClothingImage, ShippingAddress, Order, OrderItem, WishlistItem
from .forms import ClothingItemForm, CustomLoginForm, CustomSignupForm, ShippingAddressForm, ClothingItemForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
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

            # Save multiple uploaded images
            for img in request.FILES.getlist('images'):
                ClothingImage.objects.create(item=item, image=img)

            messages.success(request, "Your item has been listed successfully!")
            return redirect('item_detail', item_id=item.pk)
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        item_form = ClothingItemForm()

    return render(request, 'marketplace/create_clothing_item.html', {
        'item_form': item_form,
    })


def item_list(request):
    category = request.GET.get('category')
    items = ClothingItem.objects.all()

    if category == 'baby':
        items = items.filter(age_group='baby')
    elif category == 'toddler':
        items = items.filter(age_group='toddler')
    elif category == 'kids':
        items = items.filter(age_group='kids')
    elif category == 'big_kids':
        items = items.filter(age_group='big_kids')

    context = {
        'items': items,
        'selected_category': category,
    }
    return render(request, 'marketplace/item_list.html', context)


def item_detail(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id)

    # Get all images for this item
    images = ClothingImage.objects.filter(item=item)

    # Get related items (same category and size, excluding current)
    related_items = ClothingItem.objects.filter(
        category=item.category,
        size=item.size
    ).exclude(id=item.id)[:4]

    # Wishlist items (if authenticated)
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = set(
            WishlistItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        )

    return render(request, 'marketplace/item_detail.html', {
        'item': item,
        'images': images,
        'wishlist_ids': wishlist_ids,
        'related_items': related_items
    })


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Called when form is valid (login success)."""
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Called when form is invalid (login failure)."""
        messages.error(self.request, "Login failed. Please check your email and password.")
        return super().form_invalid(form)


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

    latest_address = None
    if request.user.is_authenticated:
        latest_address = ShippingAddress.objects.filter(user=request.user).last()

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
        'latest_address': latest_address, 
    })


@require_POST
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    cart[item_id] = {'quantity': cart.get(item_id, {}).get('quantity', 0) + 1}
    request.session['cart'] = cart
    messages.success(request, "Item added to cart.")
    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    else:
        messages.warning(request, "Item not found in cart.")
    return redirect('cart')


@require_POST
def update_cart_quantity(request, item_id):
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if item_id in cart:
        if action == 'increase':
            cart[item_id]['quantity'] += 1
            messages.success(request, "Item quantity increased.")
        elif action == 'decrease':
            if cart[item_id]['quantity'] > 1:
                cart[item_id]['quantity'] -= 1
                messages.success(request, "Item quantity decreased.")
            else:
                messages.warning(request, "Minimum quantity is 1.")
        request.session['cart'] = cart
    else:
        messages.warning(request, "Item not found in cart.")

    return redirect('cart')


@require_POST
@login_required
def process_payment(request):
    try:
        data = json.loads(request.body)
        if data.get('confirm'):
            cart = request.session.get('cart', {})
            if not cart:
                return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

            latest_address = ShippingAddress.objects.filter(user=request.user).last()
            if not latest_address:
                return JsonResponse({'status': 'error', 'message': 'No shipping address'}, status=400)

            total_price = 0
            order = Order.objects.create(
                user=request.user,
                shipping_address=latest_address,
                total_price=0  # temporary value, to be updated below
            )

            for item_id, item_data in cart.items():
                item = get_object_or_404(ClothingItem, id=item_id)
                quantity = item_data['quantity']
                price = item.price
                total_price += price * quantity

                OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=quantity,
                    price=price
                )

            order.total_price = total_price  # set the actual total
            order.save()

            request.session['order_id'] = order.id
            request.session['cart'] = {}

            return JsonResponse({'status': 'ok'})
    except Exception as e:
        print("Error in process_payment:", e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def order_confirmation(request):
    order_id = request.session.get('order_id')

    if not order_id:
        print("No order ID in session!")
        return redirect('item_list')  # fallback if missing

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        print("Order not found!")
        return redirect('item_list')

    return render(request, 'marketplace/order_confirmation.html', {
        'order': order,
        'shipping_address': order.shipping_address,
        'items': order.items.all(),
    })


def calculate_cart_total(request):
    cart = request.session.get('cart', {})
    total = 0
    for item_id, item_data in cart.items():
        try:
            item = ClothingItem.objects.get(id=item_id)
            total += item.price * item_data['quantity']
        except ClothingItem.DoesNotExist:
            continue
    return total


@login_required
def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('cart')  # Or wherever you want to go next
    else:
        form = ShippingAddressForm()

    return render(request, 'marketplace/add_shipping_address.html', {'form': form})


@login_required
def wishlist_view(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('item')
    messages.info(request, "Here are the items in your wishlist.")
    return render(request, 'marketplace/wishlist.html', {
        'wishlist_items': wishlist_items
    })


@require_POST
@login_required
def toggle_wishlist(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, item=item)

    if not created:
        wishlist_item.delete()
        messages.info(request, f"Removed '{item.title}' from your wishlist.")
        return JsonResponse({'status': 'removed'})
    
    messages.success(request, f"Added '{item.title}' to your wishlist.")
    return JsonResponse({'status': 'added'})


def about_view(request):
    return render(request, 'marketplace/about.html')


def shipping_view(request):
    return render(request, 'marketplace/shipping.html')


def returns_view(request):
    return render(request, 'marketplace/returns.html')


def contact_view(request):
    if request.method == 'POST':
        # handle form submission logic here (email or save)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # You can email this or store it in the database
        messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
        return redirect('contact')

    return render(request, 'marketplace/contact.html')


def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'marketplace/track_order.html', {'order': order})


def search_view(request):
    query = request.GET.get('q')
    size = request.GET.get('size')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    results = ClothingItem.objects.all()

    if query:
        results = results.filter(title__icontains=query)

    if size:
        results = results.filter(size=size)

    if category:
        results = results.filter(category=category)

    if min_price:
        results = results.filter(price__gte=min_price)

    if max_price:
        results = results.filter(price__lte=max_price)

    context = {
        'query': query,
        'results': results,
        'selected_size': size,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'marketplace/search_results.html', context)
