import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.coupen import Coupon

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def coupon_page(request):
    """Display a list of valid coupons."""
    coupons = []
    try:
        now = timezone.now()
        coupons = Coupon.objects.filter(valid_from__lte=now, valid_to__gte=now)
    except Exception as e:
        messages.error(request, f"{e}")
    
    return render(request, "coupon.html", {'coupons': coupons})

@login_required
@user_passes_test(is_superuser)
def save_coupon(request):
    """Save a new coupon."""
    if request.method == 'POST':
        try:
            coupon = Coupon(
                code=request.POST.get('coupon_code'),
                discount=request.POST.get('coupon_discount'),
                valid_from=request.POST.get('coupon_valid_from'),
                valid_to=request.POST.get('coupon_valid_to')
            )
            coupon.save()
            messages.success(request, "Coupon added successfully")
        except Exception as e:
            messages.error(request, f"Error adding the coupon: {str(e)}")
    
    return redirect("coupon_page")

@login_required
@user_passes_test(is_superuser)
def update_coupon(request):
    """Update an existing coupon."""
    if request.method == 'POST':
        try:
            coupon_id = request.POST.get('coupon_id')
            coupon = Coupon.objects.get(id=coupon_id)
            coupon.code = request.POST.get('coupon_code')
            coupon.discount = request.POST.get('coupon_discount')
            coupon.valid_from = request.POST.get('coupon_valid_from')
            coupon.valid_to = request.POST.get('coupon_valid_to')
            coupon.save()
            messages.success(request, "Coupon updated successfully")
        except Coupon.DoesNotExist:
            messages.error(request, "Coupon not found")
        except Exception as e:
            messages.error(request, f"Error updating the coupon: {str(e)}")
    
    return redirect("coupon_page")

@login_required
@user_passes_test(is_superuser)
def delete_coupon(request, coupon_id):
    """Delete a coupon."""
    try:
        coupon = Coupon.objects.get(id=coupon_id)
        coupon.delete()
        messages.success(request, "Coupon deleted successfully")
    except Coupon.DoesNotExist:
        messages.error(request, "Coupon not found")
    except Exception as e:
        messages.error(request, f"Error deleting the coupon: {str(e)}")
    
    return redirect("coupon_page")


def apply_coupon(request):
    """Apply the coupon and return the discount amount."""
    if request.method == 'POST':
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code')
        now = timezone.now()

        try:
            coupon = Coupon.objects.get(code=coupon_code, valid_from__lte=now, valid_to__gte=now)
            discount = coupon.discount
            request.session['discount_percentage'] = float(discount)
            return JsonResponse({'success': True, 'discount': discount})
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid or expired coupon code.'})
