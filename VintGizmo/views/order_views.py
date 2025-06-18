import json
from django.conf import settings
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
import hmac
from decimal import Decimal
import hashlib
from ..models.models import CustomUser
from ..models.orders import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from ..models.address import Address
from ..models.cart import Cart
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from ..models.sold import SoldProduct
from ..models.variation import Variation
from django.db import transaction
from decimal import Decimal
from ..models.stocks import Stock
from ..models.order_quantity import OrderQuantity
from ..models.products import Product
from datetime import datetime,timedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.orderItem import OrderItem


def create_order(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids[]')
        address_id = request.POST.get('address_id')
        session_cart_items = request.session.get('cart', {})
        Total_order = Decimal(0)
        shipping_cost_total = Decimal(0)
        created_orders = [] 
        Total_price = Decimal(0)
        
        if not item_ids:
            messages.error(request, "No items selected.")
            return redirect('CheckOutPage')

        items = []
        if request.user.is_authenticated:
            customer_name = request.user.username
            cart_items = Cart.objects.filter(id__in=item_ids, customer=request.user)
            items = [
                {
                    'product_id': item.product.id,
                    'variation_id': item.variation.id,
                    'quantity': item.quantity,
                    'owner_id': item.owner_id,
                    'price': Decimal(item.variation.sales_price)
                }
                for item in cart_items
            ]
        else:
            customer_name = request.POST.get('name')
            items = [
                {
                    'product_id': item['product_id'],
                    'variation_id': item['variation_id'],
                    'owner_id': item['owner_id'],
                    'quantity': item['quantity'],
                    'price': Decimal(item['sales_price'])
                }
                for item_id in item_ids
                for item in session_cart_items.values() if str(item_id) == str(item['id'])
            ]

        if not items:
            messages.error(request, "Items not found in your cart.")
            return redirect('CheckOutPage')

        discount_total = Decimal(request.POST.get('discount_total', 0.0))
        address = ""
        email = ""
        phone_number = ""
        
        if request.user.is_authenticated and address_id:
            try:
                address_obj = Address.objects.get(id=address_id, user=request.user)
                address = f"{address_obj.street_address}, {address_obj.city}, {address_obj.state}, {address_obj.postal_code}"
                email = request.user.email
                phone_number = address_obj.phone_number
            except Address.DoesNotExist:
                messages.error(request, "Selected address does not exist.")
                return redirect('CheckOutPage')
        elif not request.user.is_authenticated:
            address = " ".join([
                request.POST.get('street_address'),
                request.POST.get('city'),
                request.POST.get('state'),
                request.POST.get('post_code')
            ])
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')

        total_cost_before_discount = sum(item['price'] * item['quantity'] for item in items)
        total_discount = min(total_cost_before_discount, discount_total)
        discount_per_item = total_discount / total_cost_before_discount if total_cost_before_discount > 0 else Decimal(0.0)
        discount_percentage = (discount_total / total_cost_before_discount * 100) if total_cost_before_discount > 0 else Decimal(0.0)

        total_profit = Decimal(0.0)

        with transaction.atomic():
            # Group items by product_owner_id
            items_by_owner = {}
            for item in items:
                owner_id = item['owner_id']
                if owner_id not in items_by_owner:
                    items_by_owner[owner_id] = []
                items_by_owner[owner_id].append(item)

            for owner_id, items in items_by_owner.items():
                user = CustomUser.objects.get(id=owner_id)
                order_total_before_discount = sum(item['price'] * item['quantity'] for item in items)

    # Calculate the discount for this specific order
                order_discount = order_total_before_discount * Decimal(discount_percentage/100)
                # Create the order for the owner
                order = Order.objects.create(
                    user=user,
                    phone_number=phone_number,
                    email=email,
                    total_cost=0,  # Will be updated later
                    shipping_cost=0,  # Will be updated later
                    discounts=order_discount,
                    payment_method=request.POST.get('payment_method'),
                    status='pending',
                    address=address,
                    customer_name=customer_name,
                )

                order_total = Decimal(0)
                order_shipping_cost = Decimal(0)

                for item in items:
                    discounted_price = item['price'] * (1 - discount_per_item)
                    remaining_quantity = item['quantity']
                    profit_per_item = Decimal(0.0)

                    variation = Variation.objects.get(id=item['variation_id'])
                    product = Product.objects.get(id=item['product_id'])
                    shipping_cost = (product.shipping_cost)*(item['quantity'])

                    # Create OrderItem
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        variation=variation,
                        quantity=item['quantity'],
                        price=item['price'],
                        total_price=item['price']*item['quantity'],
                        discounted_price=item['quantity']*discounted_price

                          # Will be updated later
                    )

                    order_total += (item['quantity'] * discounted_price)
                    order_shipping_cost += shipping_cost

                    stocks = Stock.objects.filter(variation_id=item['variation_id'], quantity__gt=0).order_by('date_of_store')

                    for stock in stocks:
                        if remaining_quantity <= stock.quantity:
                            profit = (discounted_price - stock.cost_price) * remaining_quantity
                            total_profit += profit
                            profit_per_item += profit

                            stock.quantity -= remaining_quantity
                            stock.save()

                            OrderQuantity.objects.get_or_create(
                                order_item=order_item,  # Reference to OrderItem
                                stock_code=stock.code,
                                defaults={'quantity': remaining_quantity}
                            )

                            break
                        else:
                            profit = (discounted_price - stock.cost_price) * stock.quantity
                            total_profit += profit
                            profit_per_item += profit

                            OrderQuantity.objects.get_or_create(
                                order_item=order_item,  # Reference to OrderItem
                                stock_code=stock.code,
                                defaults={'quantity': stock.quantity}
                            )

                            remaining_quantity -= stock.quantity
                            stock.quantity = 0
                            stock.save()

                    if variation.quantity < item['quantity']:
                        messages.error(request, "Not enough stock for variation.")
                        return redirect('CheckOutPage')

                    variation.quantity -= item['quantity']
                    variation.save()

                    # Update the profit for this order item
                    order_item.profit = profit_per_item
                    order_item.save()

                    # Save sold product
                    SoldProduct.objects.create(
                        order_item=order_item,
                        product_owner_id=user,
                        variation=variation,
                        sales_price=item['price'],
                        total_quantity=item['quantity'],
                        total_price=item['quantity'] * discounted_price,
                        profit=profit_per_item,
                        
                    )

                # Update order totals
                order.total_cost = order_total + order_shipping_cost
                order.shipping_cost = order_shipping_cost
                order.save()

                Total_order += order.total_cost
                shipping_cost_total += order_shipping_cost
                created_orders.append(order)

            # Clear cart items
            if not request.user.is_authenticated and session_cart_items:
                for item_id in item_ids:
                    if str(item_id) in session_cart_items:
                        del session_cart_items[str(item_id)]
                request.session['cart'] = session_cart_items
            else:
                Cart.objects.filter(id__in=item_ids, customer=request.user).delete()

            request.session['selected_items'] = []
        
        # Send an email to the customer
        subject = "Your Order Confirmation"
        html_message = render_to_string('Store/order_confirmation_email.html', {
            'orders': created_orders,
            'customer': customer_name,
            'total_amount':   total_cost_before_discount,
            'discount_amount': total_discount,
            'shipping_cost': shipping_cost_total,
            'address': address,
            'grand_total': Total_order,
            'order_items': [item for order in created_orders for item in OrderItem.objects.filter(order=order)]  # Add order items to context

        })
        subject1="You have a new order"
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)
        send_mail(subject1,plain_message,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER],html_message=html_message)
        # Render the success page with context data
        return render(request, 'Store/success.html', {
            'orders': created_orders,
            'customer': customer_name,
            'total_amount':   total_cost_before_discount,
            'discount_amount': total_discount,
            'shipping_cost': shipping_cost_total,
            'grand_total': Total_order,
        })

    # Handle non-POST requests
    return redirect('CheckOutPage')


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def completed_orders_page(request):
    completed_orders = Order.objects.filter(
        status="completed",
        user=request.user
    ).distinct()

    return render(request, "CompleteOrder.html", {'completed_orders': completed_orders})

@login_required
@user_passes_test(is_superuser)
def pending_orders_page(request):
    pending_orders = Order.objects.filter(
        status="pending",
        user=request.user
    ).distinct()

    return render(request, "PendingOrder.html", {'pending_orders': pending_orders})

@login_required
@user_passes_test(is_superuser)
def cancelled_orders_page(request):
    cancelled_orders = Order.objects.filter(
        status="cancelled",
        user=request.user
    ).distinct()

    return render(request, "CancelledOrder.html", {'cancelled_orders': cancelled_orders})

@login_required
@user_passes_test(is_superuser)
def shipped_orders_page(request):
    shipped_orders = Order.objects.filter(
        status="shipped",
        user=request.user
    ).distinct()

    return render(request, "ShippedOrder.html", {'shipped_orders': shipped_orders})

@login_required
@user_passes_test(is_superuser)
def change_status(request):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=request.POST.get('id'))
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()

            if new_status == 'cancelled':
                # Get all the items associated with this order
                order_items = OrderItem.objects.filter(order=order)

                for order_item in order_items:
                    variation = order_item.variation
                    variation.quantity += order_item.quantity
                    variation.save()

                    # Get all OrderQuantity instances related to the OrderItem
                    order_quantities = OrderQuantity.objects.filter(order_item=order_item)

                    for order_quantity in order_quantities:
                        stock = Stock.objects.get(code=order_quantity.stock_code)
                        stock.quantity += order_quantity.quantity
                        stock.save()
                        order_quantity.quantity = 0
                        order_quantity.save()

            messages.success(request, "Status Updated Successfully")
        except Exception as e:
            messages.error(request, f"Failed to Update Status: {e}")

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@user_passes_test(is_superuser)
def delete_order(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        order.delete()
        messages.success(request, "Order Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to Delete the Order: {e}")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@user_passes_test(is_superuser)
def get_order_id(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({'order_id': order.id})

@login_required
@user_passes_test(is_superuser)
def order_items(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        items = OrderItem.objects.filter(order=order)
        return render(request, 'OrderItem.html', {
            'order': order,
            'items': items
        })
    except Exception as e:
        messages.error(request, f"Failed to retrieve order items: {e}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

def track_order_page(request):
    return render(request,"Store/TrackOrder.html")
def track_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_number = data.get('order_number')

        try:
            # Fetch the order using the provided order number
            order = Order.objects.get(order_id=order_number)
            # Fetch all items related to the order
            items = OrderItem.objects.filter(order=order)

            # Convert items to a serializable format
            items_data = [
                {
                    'product_name': item.product.name,
                    'variation_name': item.variation.name,
                    'quantity': item.quantity,
                    'price': str(item.price),  # Convert Decimal to string for JSON serialization
                    'total_cost': str(item.total_price),  # Convert Decimal to string for JSON serialization
                    'discounted_price': str(item.discounted_price)  # Include discounted price if relevant
                }
                for item in items
            ]

            # Prepare order data
            order_data = {
                'order_number': order.order_id,
                'status': order.status,
                'discount':order.discounts,
                'items': items_data
            }

            return JsonResponse({'success': True, 'order': order_data})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
@csrf_exempt
def success_page(request):
    return render(request,'success.html')
Jazz_cash_merchant="MC118744"
Jazz_cash_password="ut3hg99sw0"
return_url="http://127..0.0.1:8000/success"
integrity_salt="xv25es3445"
def Payment(request, payment):
    pp_Amount = int(payment)
    current_datetime = datetime.now()
    pp_TxnDateTime = current_datetime.strftime('%Y%m%d%H%M%S')
    expiry_datetime = current_datetime + timedelta(hours=1)
    pp_TxnExpiryDateTime = expiry_datetime.strftime('%Y%m%d%H%M%S')
    ppTxnRefNo = "T" + pp_TxnDateTime

    post_data = {
        "pp_Version": "2.0",
        "pp_IsRegisteredCustomer": "Yes",
        "pp_ShouldTokenizeCardNumber": "Yes",
        "pp_TxnType": "MPAY",
        "pp_TxnRefNo": ppTxnRefNo,
        "pp_MerchantID": Jazz_cash_merchant,
        "pp_Password": Jazz_cash_password,
        "pp_Amount": pp_Amount,
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": pp_TxnDateTime,
        "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
        "pp_BillReference": "billRef",
        "pp_Description": "Description of transaction",
        "pp_CustomerCardNumber": "5123456789012346",
        "pp_UsageMode": "API",
        "pp_ReturnURL": return_url,
        "pp_SecureHash": "",
    }

    # Generate the SecureHash
    sorted_string = "&".join(f"{key}={value}" for key, value in sorted(post_data.items()) if value != "")
    pp_SecureHash = hmac.new(
        integrity_salt.encode(),
        sorted_string.encode(),
        hashlib.sha256
    ).hexdigest()
    post_data['pp_SecureHash'] = pp_SecureHash

    # Pass data to the template
    context = {
        'post_data': post_data,
        'action_url': "https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagment/merchantform/"
    }
    return render(request, "payment_form.html", context)