from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from ..models.products import Product
from ..models.variation import Variation
from ..models.cart import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from decimal import Decimal
import uuid

from django.contrib.auth.signals import user_logged_in
def CartPage(request):
    cart_items = []
    subtotal = 0.0
    discount_percentage = 0.0  # Initialize discount percentage
    shipping_cost=0

    if request.user.is_authenticated:
        # Fetch cart items from the database for authenticated users
        cart_items = Cart.objects.filter(customer=request.user).select_related('product', 'variation').prefetch_related('variation__images')

        for item in cart_items:
            first_image = item.variation.images.first() if item.variation else item.product.images.first()
            item.first_image = first_image.image.url if first_image else None  # Assign the first image URL or None
            item.name = item.variation.name if item.variation else item.product.name  # Fetch the variation or product name
            item.sales_price = item.variation.sales_price if item.variation else item.product.sales_price  # Fetch the sales price
            item.total_price = item.quantity * item.sales_price  # Calculate the total price
            item.shipping_cost=item.product.shipping_cost
            subtotal += float(item.total_price)  # Add to subtotal
            shipping_cost+=(item.product.shipping_cost*item.quantity)

    else:
        # Fetch cart items from the session for unauthenticated users
        session_cart = request.session.get('cart', {})
        for key, item in session_cart.items():
            cart_item = {
                'id': item.get('id'),
                'product_id': item.get('product_id'),
                'variation_id': item.get('variation_id'),
                'owner_id': item.get('owner_id'),
                'name': item.get('name', 'Unknown Product'),  # Using get to avoid KeyError
                'first_image': item.get('first_image'),
                'sales_price': float(item.get('sales_price', '0')),
                'quantity': int(item.get('quantity', 1)),
                'total_price': int(item.get('quantity', 1)) * float(item.get('sales_price', '0'))
                ,'shipping_cost':item.get('shipping_cost')
            }
            cart_items.append(cart_item)
            subtotal += cart_item['total_price'] 
            product=Product.objects.get(id=cart_item['product_id'])
            print(product)
            shipping_cost+=(product.shipping_cost*cart_item['quantity'])

    # Add discount percentage if available
    discount_percentage = request.session.get('discount_percentage', 0.0)

    return render(request, 'Store/Cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_percentage': discount_percentage,
          'shipping_cost' :shipping_cost 
    })




def add_to_cart(request, product_id, variation_id):
    product = get_object_or_404(Product, id=product_id)
    variation = get_object_or_404(Variation, id=variation_id) if variation_id else None
    shipping_cost=product.shipping_cost
    quantity = int(request.POST.get('quantity', 1))
    if(quantity<0 or quantity>variation.quantity):
                return JsonResponse({'success': False, 'message': 'Enter valid quantity.'})

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            customer=request.user,
            product=product,
            variation=variation,
            owner=product.user,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if(cart_item.quantity>variation.quantity):
                                return JsonResponse({'success': False, 'message': 'Enter valid quantity.'})
            
            cart_item.save()

        return JsonResponse({'success': True, 'message': 'Item added to cart.'})
    
    else:
        # Create a unique key for the session cart item
        cart = request.session.get('cart', {})
        
        item_found = False
        for key, item in cart.items():
            if item['product_id'] == product_id and (item['variation_id'] == variation_id or (variation_id is None and item['variation_id'] is None)):
                if(item['quantity']+quantity>variation.quantity):
                                     return JsonResponse({'success': False, 'message': 'Enter valid quantity.'})

                item['quantity'] += quantity
                item['Total_price'] = item['quantity'] * float(item['sales_price'])
                item_found = True
                break
        
        if not item_found:
            if 'cart_counter' not in request.session:
                request.session['cart_counter'] = 1  # Initialize counter if not already present
            
            unique_id = request.session['cart_counter']
            request.session['cart_counter'] += 1  # Increment counter for the next item
            
            cart[unique_id] = {
                'id': unique_id,
                'product_id': product_id,
                'owner_id':product.user.id,
                'variation_id': variation_id,
                'quantity': quantity,
                'name': variation.name if variation else product.name,
                'sales_price': str(variation.sales_price) if variation else str(product.sales_price),
                'Total_price': quantity * float(variation.sales_price) if variation else quantity * float(product.sales_price),
                'first_image': variation.images.first().image.url if variation and variation.images.exists() else product.images.first().image.url if product.images.exists() else None,
                'shipping_cost':shipping_cost
            }
        
        request.session['cart'] = cart
        request.session.modified = True  # Mark session as modified to ensure changes are saved
        return JsonResponse({'success': True, 'message': 'Item added to cart.'})



def update_cart_item(request, cart_item_id):
    try:
        new_quantity = int(request.POST.get('quantity', 1))
        print(new_quantity)
        if new_quantity <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid quantity'})

        if request.user.is_authenticated:
            cart_item = get_object_or_404(Cart, id=cart_item_id, customer=request.user)
            available_quantity=cart_item.variation.quantity
            
            if new_quantity<=available_quantity:
                 cart_item.quantity = new_quantity
                 cart_item.save()
                 return JsonResponse({'success': True, 'new_quantity': new_quantity})
            else:
                 return JsonResponse({'success': False, 'error': 'Invalid quantity'})

            
            
        else:
            # Handle session cart
            session_cart = request.session.get('cart', {})
            
            if str(cart_item_id) in session_cart:# Ensure id is compared as a string
                variation_id=session_cart[str(cart_item_id)]['variation_id']
                variation_id=int(variation_id)
                variation=Variation.objects.get(id=variation_id)  
                available_quantity=variation.quantity
                if new_quantity > 0 and new_quantity<=available_quantity:
                    session_cart[str(cart_item_id)]['quantity'] = new_quantity
                    session_cart[str(cart_item_id)]['Total_price'] = new_quantity * float(session_cart[str(cart_item_id)]['sales_price'])
                    request.session['cart'] = session_cart
                    print(new_quantity)
                    return JsonResponse({'success': True, 'new_quantity': new_quantity})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid quantity'})
            else:
                return JsonResponse({'success': False, 'error': 'Cart item not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def delete_cart_item(request, id):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                cart_item = Cart.objects.get(id=id, customer=request.user)
                quantity = cart_item.quantity  # Get the quantity of the item to be deleted
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'message': 'Item deleted successfully',
                    'quantity': quantity  # Include the quantity in the response
                })
            except Cart.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)
        else:
            session_cart = request.session.get('cart', {})
            # Ensure the ID is a string when checking the session cart
            str_id = str(id)
            if str_id in session_cart:
                quantity = session_cart[str_id]['quantity']  # Get the quantity of the item to be deleted
                del session_cart[str_id]
                request.session['cart'] = session_cart
                return JsonResponse({
                    'success': True,
                    'message': 'Item deleted successfully',
                    'quantity': quantity  # Include the quantity in the response
                })
            else:
                return JsonResponse({'success': False, 'message': 'Item not found in session cart'}, status=404)
    else:
        return HttpResponseForbidden('Invalid request method')
def merge_cart_on_login(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})
    for key, value in session_cart.items():
        product = get_object_or_404(Product, id=value['product_id'])
        variation = get_object_or_404(Variation, id=value['variation_id']) if value['variation_id'] else None

        cart_item, created = Cart.objects.get_or_create(
            customer=user,
            product=product,
            variation=variation,
            owner=product.user,
            defaults={'quantity': value['quantity']}
        )

        if not created:
            cart_item.quantity += value['quantity']
            cart_item.save()

    # Clear the session cart after merging
    request.session['cart'] = {}



user_logged_in.connect(merge_cart_on_login)