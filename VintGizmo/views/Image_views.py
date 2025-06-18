from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models.products import Product
from ..models.images import Images
from ..models.variation import Variation

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def add_image(request):
    if request.method == 'POST':
        try:
            img = request.FILES.get('product_image')
            variation_id = request.POST.get('id')
            if not variation_id:
                raise ValueError("variation ID is missing")
            
            variation_instance = Variation.objects.get(pk=variation_id)
            product_id=variation_instance.product_id.id
            image = Images(
                product=variation_instance,
                image=img
            )
            image.save()
            messages.success(request, "Image added successfully")
        except Product.DoesNotExist:
            messages.error(request, "Variation does not exist")
        except Exception as e:
            messages.error(request, f"Failed to add the image: {str(e)}")
    else:
        messages.error(request, 'Invalid request method')

    return redirect('DetailPage',id=product_id)

@login_required
@user_passes_test(is_superuser)
def DeleteImage(request,id):
   image = get_object_or_404(Images, id=id)
   variation=image.product.id
   try:
     

    
     image.delete()
     messages.success(request,"Image deleted successfully")
   except:
    messages.error(request,"Failed to delete the image")
  
   return redirect('V_D',id=variation)
