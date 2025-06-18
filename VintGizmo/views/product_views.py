from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from ..models.products import Product
from ..models.category import Category
from ..models.brand import Brand
from ..models.stocks import Stock
from ..models.sold import SoldProduct

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def Product_Page(request):
    """Display product page with categories, brands, and products."""
    user=request.user
    categories = Category.objects.filter(user_id=user)
    brands = Brand.objects.filter(user_id=user)
    products = Product.objects.filter(user_id=user)

    context = {
        'categories': categories,
        'brands': brands,
        'products': products
    }
    return render(request, 'Products.html', context)

@login_required
@user_passes_test(is_superuser)
def SaveProduct(request):
    """Save a new product."""
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            category_instance = Category.objects.get(pk=category_id)
            brand_id = request.POST.get('brand')
            brand_instance = Brand.objects.get(pk=brand_id)
            shipping_cost = request.POST.get('shipping_cost')
            data = request.POST

            # Create the Product instance
            product = Product(
                user=request.user,
                name=data.get('name'),
                category=category_instance,
                brand=brand_instance,
                shipping_cost=shipping_cost
            )
            product.full_clean()
            product.save()

            messages.success(request, "Product added successfully")
            return redirect('product_management')
        except Exception as e:
            messages.error(request, f"Failed to add Product: {str(e)}")
            return redirect('product_management')
    else:
        messages.error(request, "Invalid request method")
        return redirect('product_management')

@login_required
@user_passes_test(is_superuser)
def update_product(request):
    """Update an existing product."""
    if request.method == 'POST':
        try:
            product_id = request.POST.get('id')
            product = get_object_or_404(Product, id=product_id)
            category_id = request.POST.get('category')
            category_instance = Category.objects.get(pk=category_id)
            brand_id = request.POST.get('brand')
            brand_instance = Brand.objects.get(pk=brand_id)
            shipping_cost = request.POST.get('shipping_cost')
            data = request.POST

            # Update product fields
            product.name = data.get('name')
            product.category = category_instance
            product.brand = brand_instance
            product.shipping_cost = shipping_cost

            product.full_clean()
            product.save()
            messages.success(request, "Product updated successfully")
            return redirect('product_management')
        except Exception as e:
            messages.error(request, f"Failed to update product: {str(e)}")
            return redirect('product_management')
    else:
        messages.error(request, "Invalid request method")
        return redirect('product_management')

@login_required
@user_passes_test(is_superuser)
def delete_product(request, id):
    """Delete a product."""
    try:
        product = get_object_or_404(Product, id=id)
        product.delete()
        messages.success(request, "Product deleted successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete product: {str(e)}")
    return redirect('product_management')

@login_required
@user_passes_test(is_superuser)
def get_product_data(request, id):
    """Retrieve product data for a specific product."""
    try:
        product = get_object_or_404(Product, id=id)
        product_data = {
            'name': product.name,
            'brand_id': product.brand.id,
            'category_id': product.category.id,
            'id': product.id
        }
        return JsonResponse(product_data, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@login_required
@user_passes_test(is_superuser)

def sold_products(request):
    """Display sold products for the logged-in user."""
    sold_products = SoldProduct.objects.filter(
        product_owner_id=request.user
    ).exclude(
        order_item__order__status='cancelled'
    )
    return render(request, 'SoldProduct.html', {'sold_products': sold_products})
