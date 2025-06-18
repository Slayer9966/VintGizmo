from audioop import avg
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.products import Product
from ..models.variation import Variation
from django.shortcuts import get_object_or_404, redirect
from ..models.models import CustomUser
from django.db.models import Avg
from ..models.store_review import StoreReview
from ..models.Banner import HomeBanner
from ..models.homeImage import homeImage
from ..models.SaleBanner import SaleBanner
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models.functions import Lower, Replace
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from ..models.orders import Order


def dynamic_css(request):
    # Example data to pass to the template
    sale=SaleBanner.objects.first()
    home=HomeBanner.objects.first()
    sale = {
        'background': sale.background,  # This would typically come from your database
        'main_text_color': sale.main_text_color,
        'secondry_color': sale.secondry_color,
        'button_background': sale.button_background,
        'button_text': sale.button_text,
        'homeMain':home.main_text_color,
        'homesecond':home.secondry_text,
        'buttonbackground':home.button_background,
        
    }

    # Render the CSS template with context
    css = render_to_string('Store/dynamic.css', {'sale': sale})
    
    # Return the response with the correct MIME type
    return HttpResponse(css, content_type='text/css')


def HomePage(request):
    user_id = request.session.get('user_id')
    user = None
    products_with_variations = []
    top_rated_products_with_variations = []
    store_reviews_approved = []
    homebanner = None
    sale = None
    images = []

    try:
        if user_id:
            user = CustomUser.objects.get(id=user_id)

        # Fetch the latest 8 products
        homebanner = HomeBanner.objects.first()  
        sale = SaleBanner.objects.first()
        images = homeImage.objects.all()
        products = Product.objects.all().order_by('-created_at')[:8]
        
        for product in products:
            first_variation = Variation.objects.filter(product_id=product).first()
            if first_variation:
                first_image = first_variation.images.first()  # Get the first image associated with the variation
                products_with_variations.append({
                    'product': product,
                    'variation': first_variation,
                    'image': first_image
                })

        # Fetch products with the highest average rating of all variations
        highest_rated_products = Product.objects.annotate(
    average_rating=Avg('products__ratings_reviews__rating')  # Aggregating ratings from related variations
).filter(
    average_rating__isnull=False,  # Exclude products with no ratings
    average_rating__gt=0  # Exclude products with zero average rating
).order_by('-average_rating')[:6]

        top_rated_products_with_variations = []

        for product in highest_rated_products:
    # Get the first variation for each product
          first_variation = Variation.objects.filter(product_id=product).first()
          if first_variation:
              first_image = first_variation.images.first()  # Get the first image for the variation
              top_rated_products_with_variations.append({
            'product': product,
            'variation': first_variation,
            'image': first_image,
            'average_rating': product.average_rating  # Annotated average rating
        })

# Sorting is optional since the queryset is already ordered
        top_rated_products_with_variations.sort(key=lambda x: x['average_rating'] if x['average_rating'] is not None else 0, reverse=True)

        # Fetch approved store reviews
        store_reviews_approved = StoreReview.objects.filter(status='approved')
        print(store_reviews_approved)

    except CustomUser.DoesNotExist:
        # User not found, user will remain None
        pass

    # Render the index.html with user context, latest products, and highest-rated products
    return render(request, 'store/index.html', {
        'user': user,
        'products_with_variations': products_with_variations,
        'top_rated_products_with_variations': top_rated_products_with_variations,
        'store_reviews_approved': store_reviews_approved,
        'homebanner': homebanner,
        'images': images,
        'sale': sale
    })

def ProductPage(request):
    query = request.GET.get('q')  # Get the search keyword from the request
    products_with_variations = []

    if query:
        # If a search query is provided, filter products based on the keyword
        query = query.lower().strip()
        keywords = query.split()  # Split the query into individual keywords

        # Start with an empty Q object
        query_filter = Q()

        # Create a Q object for each keyword
        for keyword in keywords:
            query_filter |= Q(name__icontains=keyword)

        # Filter products using the combined Q object
        products = Product.objects.filter(query_filter)
    else:
        query=""
        # If no search query, return all products
        products = Product.objects.all()

    for product in products:
        first_variation = Variation.objects.filter(product_id=product).first()
        if first_variation:
            first_image = first_variation.images.first()  # Get the first image associated with the variation
            products_with_variations.append({
                'product': product,
                'variation': first_variation,
                'image': first_image  # Add the first image to the context
            })

    context = {
        'products_with_variations': products_with_variations,
        'query': query  # Pass the query back to the template
    }
    
    return render(request, 'Store/products.html', context)

def ProductDetail(request, id):
    # Fetch the main product based on the provided id
    product = get_object_or_404(Product, id=id)
    
    # Fetch all variations of the product and prefetch related images
    variations = Variation.objects.filter(product_id=id).prefetch_related('images')
    first_variation = variations.first()  # First variation of the main product

    # Calculate the average rating for the first variation
    average_rating = first_variation.ratings_reviews.aggregate(Avg('rating'))['rating__avg'] if first_variation else 0
    average_rating = round(average_rating or 0)  # Round to the nearest integer
    
    # Generate a list of numbers from 1 to 5 for the stars
    star_range = range(1, 6)

    # Get the category of the current product
    category = product.category

    # Fetch related products in the same category, excluding the current product
    related_products = Product.objects.filter(category=category).exclude(id=id)
    
    # Prepare the related products with their first variations and images
    products_with_variations = []
    for related_product in related_products:
        first = Variation.objects.filter(product_id=related_product.id).first()
        if first:
            first_image = first.images.first()  # Get the first image associated with the variation
            products_with_variations.append({
                'product': related_product,
                'variation': first_variation,
                'image': first_image  # Add the first image to the context
            })

    # Pass the main product, its variations, and related products with variations to the template
    return render(request, 'store/ProductDetail.html', {
        'product': product,
        'variations': variations,
        'first_variation': first_variation,
        'products_with_variations': products_with_variations,
        'average_rating': average_rating,
        'star_range': star_range,  # Pass the star range
    })



def get_variation_details(request, id):
    try:
        variation = Variation.objects.get(id=id)
        
        # Calculate the average rating for the variation
        average_rating = variation.ratings_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        average_rating = round(average_rating)  # Round to the nearest integer
        
        data = {
            'name': variation.name,
            'sales_price': variation.sales_price,
            'description': variation.description,
            'id': variation.id,
            'average_rating': average_rating,  # Add average rating to the response
            'images': [{'url': image.image.url} for image in variation.images.all()]
        }
        return JsonResponse(data)
    except Variation.DoesNotExist:
        return JsonResponse({'error': 'Variation not found'}, status=404)
    

def privacy_policy_page(request):
    return render(request,"Store/PrivacyPolicy.html")
def terms_of_use_page(request):
    return render(request,"Store/TermsOfUse.html")
def refund_page(request):
    return render(request,"Store/ReturnRefund.html")
def contact_us_page(request):
    return render(request,"Store/Contact.html")

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Email details
        subject = f"Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.EMAIL_HOST_USER]  # Send to the same email address as EMAIL_HOST_USER

        try:
            send_mail(subject, body, from_email, to_email)
            return JsonResponse({'success': True, 'message': 'Email sent successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def user_profile_page(request):
    return render(request, 'Store/Profile.html')
def profile_save(request):
    if request.method == 'POST':
        user = request.user
        user.Phone_Number = request.POST['Phone_Number']
        user.username = request.POST['username']
        
        if 'User_Profile_Pic' in request.FILES:
            user.User_Profile_Pic = request.FILES['User_Profile_Pic']
        
        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')

    return redirect('profile')

def user_orders_view(request):
    if request.user.is_authenticated:
        user = request.user

        # Fetch orders for each status
        pending_orders = Order.objects.filter(user=user, status='pending').prefetch_related('items')
        shipped_orders = Order.objects.filter(user=user, status='shipped').prefetch_related('items')
        delivered_orders = Order.objects.filter(user=user, status='delivered').prefetch_related('items')
        cancelled_orders = Order.objects.filter(user=user, status='cancelled').prefetch_related('items')
        all_orders = Order.objects.filter(user=user).prefetch_related('items')
    
    else:
        # In case the user is not authenticated, ensure the lists are empty
        pending_orders = []
        shipped_orders = []
        delivered_orders = []
        cancelled_orders = []
        all_orders = []

    # Determine the current status filter based on the GET parameter
    status = request.GET.get('status', 'all')  # Default to 'all' if no status is provided

    # Select the correct orders list based on the status filter
    orders = {
        'all': all_orders,
        'pending': pending_orders,
        'shipped': shipped_orders,
        'delivered': delivered_orders,
        'cancelled': cancelled_orders,
    }.get(status, all_orders)

    context = {
        'orders': orders,
        'status': status,
    }

    return render(request, 'Store/Orders.html', context)

