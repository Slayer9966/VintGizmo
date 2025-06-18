from datetime import datetime, timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from ..models.products import Product
from ..models.category import Category
from ..models.brand import Brand
from ..models.stocks import Stock
import random
from django.db.models import Sum
from django.contrib.auth.decorators import login_required,user_passes_test
from ..models.variation import Variation
from ..models.products import Product
from datetime import date
import random, string

def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def detail_page(request, id):
    """View to display details of a product."""
    product = get_object_or_404(Product, id=id)
    variations = Variation.objects.filter(product_id=product.id)
    return render(request, "ProductDetails.html", {'product': product, 'variations': variations})

@login_required
@user_passes_test(is_superuser)
def add_variation(request):
    """View to add a new product variation."""
    if request.method == 'POST':
        name = request.POST.get('name')
        product_id = request.POST.get('product_id')
        cost_price = request.POST.get('cost_price')
        sales_price = request.POST.get('sales_price')
        sale_price = request.POST.get('sale_price')
        warranty = request.POST.get('warranty')
        description = request.POST.get('description')
        quantity = int(request.POST.get('quantity', 0))

        try:
            product = Product.objects.get(id=product_id)
            variation = Variation.objects.create(
                product_id=product,
                quantity=quantity,
                cost_price=cost_price,
                sales_price=sales_price,
                sale_price=sale_price,
                warranty=warranty,
                description=description,
                name=name
            )
            Stock.objects.create(
                variation_id=variation,
                cost_price=cost_price,
                sales_price=sales_price,
                quantity=quantity,
                total_quantity=quantity,
                date_of_store=datetime.now().date()
            )
            messages.success(request, "Variation added successfully")
        except Product.DoesNotExist:
            messages.error(request, "Product not found")
        except Exception as e:
            messages.error(request, f"Failed to add variation: {str(e)}")

        return redirect('DetailPage', id=product_id)

    return redirect('DetailPage', id=request.POST.get('product_id'))

@login_required
@user_passes_test(is_superuser)
def update_variation(request):
    """View to update an existing product variation."""
    if request.method == 'POST':
        variation_id = request.POST.get('id')
        variation = get_object_or_404(Variation, id=variation_id)
        product_id = variation.product_id.id

        try:
            cost_price = request.POST.get('cost_price')
            sales_price = request.POST.get('sales_price')
            sale_price = request.POST.get('sale_price')
            warranty = request.POST.get('warranty')
            description = request.POST.get('description')
            new_quantity = int(request.POST.get('quantity', 0))
            stock_option = request.POST.get('stock_option')

            variation.cost_price = cost_price
            variation.sales_price = sales_price
            variation.sale_price = sale_price
            variation.warranty = warranty
            variation.description = description
            variation.save()

            if stock_option == 'add_new_stock':
                Stock.objects.create(
                    variation_id=variation,
                    cost_price=cost_price,
                    sales_price=sales_price,
                    quantity=new_quantity,
                    total_quantity=new_quantity,
                    date_of_store=datetime.now().date()
                )
            elif stock_option == 'add_to_existing_stock':
                last_stock = Stock.objects.filter(variation_id=variation).order_by('-date_of_store').first()
                if last_stock:
                    last_stock.quantity += new_quantity
                    last_stock.total_quantity += new_quantity
                    last_stock.cost_price = cost_price
                    last_stock.sales_price = sales_price
                    last_stock.date_of_store = datetime.now().date()
                    last_stock.save()
            elif stock_option == 'update_the_quantity':
                last_stock = Stock.objects.filter(variation_id=variation).order_by('-date_of_store').first()
                if last_stock:
                    last_stock.quantity = new_quantity
                    last_stock.total_quantity = new_quantity
                    last_stock.cost_price = cost_price
                    last_stock.sales_price = sales_price
                    last_stock.date_of_store = datetime.now().date()
                    last_stock.save()
            elif stock_option == 'no_change_stock':
                last_stock = Stock.objects.filter(variation_id=variation).order_by('-date_of_store').first()
                if last_stock:
                    last_stock.cost_price = cost_price
                    last_stock.sales_price = sales_price
                    last_stock.date_of_store = datetime.now().date()
                    last_stock.save()

            total_quantity = Stock.objects.filter(variation_id=variation).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            variation.quantity = total_quantity
            variation.save()
            messages.success(request, "Variation updated successfully")
        except Exception as e:
            messages.error(request, f"Failed to update the variation: {str(e)}")
            return redirect('DetailPage')
        
        return redirect('DetailPage', id=product_id)
    
    messages.error(request, "Invalid request method")
    return redirect('DetailPage', id=request.POST.get('product_id'))

@login_required
@user_passes_test(is_superuser)
def delete_variation(request, id):
    """View to delete a product variation."""
    variation = get_object_or_404(Variation, id=id)
    product_id = variation.product_id.id

    try:
        variation.delete()
        messages.success(request, "Variation deleted successfully")
    except Variation.DoesNotExist:
        messages.error(request, "Variation not found")
    except Exception as e:
        messages.error(request, f"Failed to delete variation: {str(e)}")
    
    return redirect('DetailPage', id=product_id)

@login_required
@user_passes_test(is_superuser)
def get_variation_data(request, id):
    """View to get data for a specific variation."""
    try:
        variation = get_object_or_404(Variation, id=id)
        variation_data = {
            'name': variation.name,
            'sales_price': variation.sales_price,
            'sale_price': variation.sale_price,
            'cost_price': variation.cost_price,
            'warranty': variation.warranty,
            'description': variation.description,
            'quantity': variation.quantity,
            'id': variation.id
        }
        return JsonResponse(variation_data, status=200)
    except Variation.DoesNotExist:
        return JsonResponse({'error': 'Variation not found'}, status=404)