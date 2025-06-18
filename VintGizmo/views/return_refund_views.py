from datetime import datetime, timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from ..models.products import Product
from ..models.category import Category
from ..models.brand import Brand
from ..models.stocks import Stock
from ..models.return_refund import ReturnRefund
import random
from ..models.orders import Order
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def create_return_request(request, order_id):
    # Get the Order object
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Capture the reason for the return from the POST data
        reason = request.POST.get('reason', '')

        # Create the return request
        return_request = ReturnRefund.objects.create(
            order=order,
            user=request.user,  # Assuming the user is logged in
            reason=reason,
            return_requested_at=timezone.now(),
            return_status='Pending',  # Default status is pending
        )

        # Optionally, you can add notes or handle other fields as needed

        # Add a success message
        messages.success(request, 'Your return request has been submitted successfully.')

        # Redirect to a success page or the order details page
        return redirect('order_details', order_id=order.id)
    
    # If it's a GET request, you can render a template with a form to submit the return request
    return render(request, 'your_template_name.html', {'order': order})