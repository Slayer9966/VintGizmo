from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.products import Product
from ..models.images import Images
from ..models.variation import Variation
from ..models.stocks import Stock

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def Product_V_D_Page(request, id):
    """Display product variation details including stocks and images."""
    try:
        stocks = Stock.objects.filter(variation_id=id)
        images = Images.objects.filter(product=id)

        return render(request, "ProductVariationDetail.html", {"stocks": stocks, "images": images})
    except Exception as e:
        messages.error(request, f"Failed to retrieve product variation details: {str(e)}")
        return redirect('product_management')
