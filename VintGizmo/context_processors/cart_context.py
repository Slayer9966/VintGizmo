from ..models.cart import Cart
from django.db.models import Sum


def cart_total_quantity(request):
    total_quantity = 0

    if request.user.is_authenticated:
        # For authenticated users, calculate the total quantity from the database
        total_quantity = Cart.objects.filter(customer=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        # For unauthenticated users, calculate the total quantity from the session
        if 'cart' in request.session:
            for item in request.session['cart'].values():
                total_quantity += item['quantity']

    return {
        'cart_total_quantity': total_quantity
    }
