from django.shortcuts import get_object_or_404, redirect, render
from ..models.SaleBanner import SaleBanner
from ..models.homeImage import homeImage
from ..models.Banner import HomeBanner
from django.contrib import messages
import os

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, redirect, render

def superuser_required(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(superuser_required)
def destroy_home_banner(request):
    try:
        banner = HomeBanner.objects.first()
        image_path = banner.banner_image.path
            
            # Delete the banner record
        banner.delete()
            
            # Delete the image file from the server
        if os.path.exists(image_path):
                os.remove(image_path)
        

        messages.success(request, "Banner deleted Successfully")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('home_banner')

@user_passes_test(superuser_required)
def save_home_banner(request):
    if request.method == 'POST':
        try:
            main_text = request.POST.get('main_text')
            secondry_text = request.POST.get('secondry_text')
            banner_image = request.FILES.get('banner_image')
            main_text_color = request.POST.get('main_text_color')
            button_background = request.POST.get('button_background')
            button_color = request.POST.get('button_color')
            button_text = request.POST.get('button_text')

            if main_text and secondry_text and banner_image:
                banner = HomeBanner(
                    main_text=main_text,
                    secondry_text=secondry_text,
                    banner_image=banner_image,
                    main_text_color=main_text_color,
                    button_background=button_background,
                    button_color=button_color,
                    button_text=button_text
                )
                banner.save()
                messages.success(request, "Banner added successfully")
            else:
                messages.error(request, "All fields are required.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('home_banner')

@user_passes_test(superuser_required)
def save_sale_banner(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            second_text = request.POST.get('second_text')
            paragraph = request.POST.get('paragraph')
            sale_str = request.POST.get('sale')
            image = request.FILES.get('image')
            background = request.POST.get('background')
            main_text_color = request.POST.get('main_text_color')
            secondry_color = request.POST.get('secondry_color')
            button_background = request.POST.get('button_background')
            button_text = request.POST.get('button_text')

            try:
                sale = int(sale_str)
            except (ValueError, TypeError):
                messages.error(request, "Sale percentage must be an integer between 0 and 100.")
                return redirect('sale_banner')

            if not title or not second_text or not paragraph or not sale_str:
                messages.error(request, "All fields are required.")
                return redirect('sale_banner')

            if sale < 0 or sale > 100:
                messages.error(request, "Sale percentage must be between 0 and 100.")
                return redirect('sale_banner')

            sale_banner = SaleBanner(
                title=title,
                second_text=second_text,
                paragraph=paragraph,
                sale=sale,
                image=image,
                main_text_color=main_text_color,
                background=background,
                secondry_color=secondry_color,
                button_background=button_background,
                button_text=button_text
            )

            sale_banner.save()
            messages.success(request, "Banner saved successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('sale_banner')

@user_passes_test(superuser_required)
def delete_sale_banner(request):
    try:
        sale_banner = SaleBanner.objects.first()
        imagepath=sale_banner.image.path
        sale_banner.delete()
        if os.path.exists(imagepath):
                os.remove(imagepath)
        messages.success(request, "Banner deleted successfully")
    except SaleBanner.DoesNotExist:
        messages.error(request, "Banner not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('sale_banner')

@user_passes_test(superuser_required)
def save_home_image(request):
    if request.method == 'POST':
        try:
            image_text = request.POST.get('image_text')
            image = request.FILES.get('image')

            if not image_text or not image:
                messages.error(request, "Image text and image are required.")
                return redirect('home_images')

            home_image = homeImage(image_text=image_text, image=image)
            home_image.save()
            messages.success(request, "Home image saved successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home_images')
    return redirect('home_images')

@user_passes_test(superuser_required)
def update_home_image(request):
    try:
        image_id = request.POST.get('home_image_id')
        home_image = get_object_or_404(homeImage, id=image_id)

        if request.method == 'POST':
            image_text = request.POST.get('image_text')
            new_image = request.FILES.get('image')

            # Update image text if provided
            if image_text:
                home_image.image_text = image_text

            # Handle image update
            if new_image:
                # Delete the previous image file from the server
                if home_image.image and os.path.isfile(home_image.image.path):
                    os.remove(home_image.image.path)

                # Set the new image
                home_image.image = new_image

            # Save changes
            home_image.save()
            messages.success(request, "Home image updated successfully.")
        
        return redirect('home_images')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home_images')

@user_passes_test(superuser_required)
def delete_home_image(request, image_id):
    try:
        home_image = get_object_or_404(homeImage, id=image_id)
        if home_image.image and os.path.isfile(home_image.image.path):
            os.remove(home_image.image.path)

        # Delete the HomeImage record
        home_image.delete()
        
        messages.success(request, "Home image deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('home_images')

@user_passes_test(superuser_required)
def HomeBannerPage(request):
    try:
        banner = HomeBanner.objects.first()
    except:
        banner = None
        messages.info(request, "No Home Banner found.")

    return render(request, "HomeBanner.html", {'banner': banner})

@user_passes_test(superuser_required)
def SaleBannerPage(request):
    try:
        sale_banner = SaleBanner.objects.first()
    except:
        sale_banner = None
        messages.info(request, "No Sale Banner found.")

    return render(request, "SaleBanner.html", {'sale_banner': sale_banner})

@user_passes_test(superuser_required)
def HomeImagesPage(request):
    try:
        home_images = homeImage.objects.all()
        if not home_images:
            messages.info(request, "No Home Images found.")
    except Exception as e:
        home_images = []
        messages.error(request, f"An error occurred: {str(e)}")
    return render(request, "HomeImages.html", {'home_images': home_images})
