from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from VintGizmo.models.models import CustomUser
from django.http import JsonResponse
from django.db.models import Sum
from ..models.sold import SoldProduct
from django.db.models.functions import TruncYear, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    # Retrieve user ID from session
    user_id = request.session.get('user_id')
    
    # Fetch user details from the database
    user = get_object_or_404(CustomUser, id=user_id)

    # Get the current date
    today =timezone.localtime().date()

    # Filter sold products for today using the Order's created_at date through OrderItem
    today_sales_data = SoldProduct.objects.filter(
        product_owner_id=user,
        order_item__order__created_at__date=today  # Filter by today's date using the Order's created_at field
    ).exclude(
        order_item__order__status='cancelled'  # Exclude cancelled orders based on Order's status
    ).aggregate(
        total_sales=Sum('total_price'),
        total_profit=Sum('profit')
    )
    print(today)
    # Debug: Print the aggregated sales data for today
    print(f"Today's Sales Data: {today_sales_data}")

    # Filter all sold products for overall sales and profit, excluding cancelled orders
    overall_sales_data = SoldProduct.objects.filter(
        product_owner_id=user
    ).exclude(
        order_item__order__status='cancelled'  # Exclude cancelled orders
    ).aggregate(
        total_sales=Sum('total_price'),
        total_profit=Sum('profit')
    )
    
    # Prepare the context with calculated values
    context = {
        'user': user,
        'today_sales': today_sales_data['total_sales'] or 0,
        'today_profit': today_sales_data['total_profit'] or 0,
        'overall_sales': overall_sales_data['total_sales'] or 0,
        'overall_profit': overall_sales_data['total_profit'] or 0,
    }
    
    return render(request, 'AdminDashboard.html', context)


@login_required
@user_passes_test(is_superuser)
def annual_sales_profits(request):
    sales_data = SoldProduct.objects.filter(
        product_owner_id=request.user
    ).exclude(
        order_item__order__status='cancelled'  # Exclude cancelled orders via Order
    ).annotate(
        year=TruncYear('order_item__created_at')  # Use 'created_at' from 'OrderItem'
    ).values('year').annotate(
        total_sales=Sum('total_price'),
        total_profits=Sum('profit')
    ).order_by('year')

    labels = [str(sale['year'].year) for sale in sales_data]
    sales = [sale['total_sales'] for sale in sales_data]
    profits = [sale['total_profits'] for sale in sales_data]

    data = {
        "labels": labels,
        "salesData": sales,
        "profitsData": profits
    }
    return JsonResponse(data)

@login_required
@user_passes_test(is_superuser)
def monthly_sales_profits(request):
    current_year = timezone.now().year
    sales_data = SoldProduct.objects.filter(
        product_owner_id=request.user,
        order_item__created_at__year=current_year  # Filter by year using 'created_at' from 'OrderItem'
    ).exclude(
        order_item__order__status='cancelled'  # Exclude cancelled orders via Order
    ).annotate(
        month=TruncMonth('order_item__created_at')  # Use 'created_at' from 'OrderItem'
    ).values('month').annotate(
        total_sales=Sum('total_price'),
        total_profits=Sum('profit')
    ).order_by('month')

    labels = [sale['month'].strftime('%b') for sale in sales_data]
    sales = [sale['total_sales'] for sale in sales_data]
    profits = [sale['total_profits'] for sale in sales_data]

    data = {
        "labels": labels,
        "salesData": sales,
        "profitsData": profits
    }
    return JsonResponse(data)
