from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.brand import Brand

def superuser_required(user):
    return user.is_superuser

@login_required
@user_passes_test(superuser_required)
def SaveBrand(request):
    if request.method == 'POST':
        try:
            data = request.POST
            brand_image = request.FILES.get('brand_image')  # Handle file upload properly

            brand = Brand(
                user=request.user,
                BrandName=data.get('BrandName'),
                BrandDescription=data.get('Description'),
                BrandImage=brand_image  # Use the file from request.FILES
            )
            brand.save()
            messages.success(request, "Brand added successfully")
            return redirect('product_management')  # Return the redirect to ensure it works
        except Exception as e:
            messages.error(request, f"Failed to add brand: {str(e)}")
            return redirect('product_management')
    else:
        messages.error(request, "Invalid request method")
        return redirect('product_management')

@login_required
@user_passes_test(superuser_required)
def get_brands(request):
    if request.method == 'GET':
        # Filter brands for the currently authenticated user
        brands = Brand.objects.filter(user=request.user)
        brand_list = [
            {'id': brand.id, 'name': brand.BrandName}  # Adjust field names if needed
            for brand in brands
        ]
        return JsonResponse(brand_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
@login_required
@user_passes_test(superuser_required)
def delete_brand(request,id):
    try:
        brand=Brand.objects.filter(id=id)
        brand.delete()
        messages.success(request, "Brand deleted successfully")
        return redirect('product_management')
    except:
      messages.error(request, "Failed to Delete the brand")
      return redirect('product_management')
     
