from django.http import JsonResponse
from django.shortcuts import redirect, render
from ..models.category import Category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def SaveCategory(request):
    if request.method == 'POST':
        try:
            data = request.POST
            cat_image = request.FILES.get('cat_image')  # Handle file upload properly

            category = Category(
                user=request.user,
                name=data.get('name'),
                Description=data.get('Description'),
                Cat_Image=cat_image  # Use the file from request.FILES
            )
            category.save()
            messages.success(request, "Category added successfully")
            return redirect('product_management')
        except Exception as e:
            logger.error(f"Error adding category: {e}")
            messages.error(request, f"Failed to add Category: {str(e)}")
            return redirect('product_management')
    else:
        messages.error(request, "Invalid request method")
        return redirect('product_management')

@login_required
@user_passes_test(is_superuser)
def get_categories(request):
    if request.method == 'GET':
        # Filter categories for the currently authenticated user
        categories = Category.objects.filter(user=request.user)
        category_list = [
            {'id': category.id, 'name': category.name}
            for category in categories
        ]
        return JsonResponse(category_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@user_passes_test(is_superuser)
def delete_catogery(request,id):
    try:
        category=Category.objects.filter(id=id)
        category.delete();
        messages.success(request, "Category deleted successfully")
        return redirect('product_management')
    except:
      messages.error(request, "Failed to Delete the category")
      return redirect('product_management')