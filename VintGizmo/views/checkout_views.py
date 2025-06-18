import json
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from ..models.products import Product
from ..models.variation import Variation
from ..models.cart import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from decimal import Decimal
from ..models.address import Address
import uuid

from django.contrib.auth.signals import user_logged_in
def CheckOutPage(request):
    """
    This view displays the checkout page with only the selected items.
    """
    cart_items = []
    addresses = []
    selected_item_ids = request.session.get('selected_items', [])  # Fetch selected item IDs from session

    # Debugging statement
    print("Selected item IDs from session:", selected_item_ids)

    subtotal = 0.0
    discount_percentage = request.session.get('discount_percentage', 0.0)  # Get discount percentage from session
    shipping = 0  # Flat rate shipping cost

    if request.user.is_authenticated:
        # Fetch selected items from the database
        if selected_item_ids:
            cart_items = Cart.objects.filter(id__in=selected_item_ids, customer=request.user)\
                                     .select_related('product', 'variation')\
                                     .prefetch_related('variation__images')

            addresses = Address.objects.filter(user=request.user)

            for item in cart_items:
                # Assign the first image URL or None
                first_image = item.variation.images.first() if item.variation else item.product.images.first()
                item.first_image = first_image.image.url if first_image else None
                
                # Fetch the variation or product name
                item.name = item.variation.name if item.variation else item.product.name
                
                # Fetch the sales price
                item.sales_price = item.variation.sales_price if item.variation else item.product.sales_price
                
                # Calculate the total price
                item_total_price = item.quantity * item.sales_price
                item.total_price = item_total_price
                
                # Add to subtotal
                subtotal += float(item_total_price)
                shipping+=(item.product.shipping_cost*item.quantity)

        else:
            # Redirect to the cart page if no items are selected
            print("No selected items for authenticated user, redirecting to CartPage.")  # Debugging statement
            return redirect('CartPage')  # Replace 'CartPage' with the actual name of your cart page URL

    else:
        # For unauthenticated users, fetch cart items from the session
        session_cart = request.session.get('cart', {})

        # Debugging statement
        print("Session cart items:", session_cart)

        for key, item in session_cart.items():
            if key in selected_item_ids:  # Only include items that are in selected_item_ids
                # Safe data extraction and conversion
                item_id = item.get('id')
                name = item.get('name', 'Unknown Product')
                first_image = item.get('first_image')
                sales_price = float(item.get('sales_price', 0))
                quantity = int(item.get('quantity', 1))
                
                # Calculate total price
                total_price = quantity * sales_price
                
                # Append to cart_items list
                cart_items.append({
                    'id': item_id,
                    'name': name,
                    'first_image': first_image,
                    'sales_price': sales_price,
                    'quantity': quantity,
                    'total_price': total_price
                })
                product=Product.objects.get(id=item['product_id'])
                print(product)
                shipping+=(product.shipping_cost*item['quantity'])
                # Add to subtotal
                subtotal += total_price
        if not cart_items:
            print("No cart items for unauthenticated user, redirecting to CartPage.")  # Debugging statement
            return redirect('CartPage')  # Replace 'cart_page' with the actual name of your cart page URL

    # Calculate discount amount and total amount
    discount_amount = (subtotal * discount_percentage) / 100
    total_amount = subtotal - discount_amount + shipping

    return render(request, 'Store/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'subtotal': subtotal,
        'discount_percentage': discount_percentage,
        'discount_amount': discount_amount,
        'total_price': total_amount,
        'shipping': shipping
    })
def store_selected_items(request):
    """
    This view handles the selected items from the cart page.
    The selected item IDs are stored in the user's session.
    """
    if request.method == 'POST':
        try:
            # Parse the JSON body directly
            data = json.loads(request.body)
            selected_items = data.get('selected_items', [])
            print(selected_items)

            if selected_items:
                # Store selected item IDs in the session
                request.session['selected_items'] = selected_items
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'No items selected'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
