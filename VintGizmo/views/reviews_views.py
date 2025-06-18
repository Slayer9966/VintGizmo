from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from ..models.variation import Variation
from ..models.reviews import RatingReview
from ..models.products import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if not product_id or not rating or not review:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'})
        try:
            product = Variation.objects.get(id=product_id)
        except Variation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'})

        # Check if user has already reviewed this product
        existing_review = RatingReview.objects.filter(product=product, user=request.user).first()
        if existing_review:
            existing_review.rating = rating
            existing_review.review = review
            existing_review.save()
        else:
            RatingReview.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                review=review
            )

        return JsonResponse({'status': 'success', 'message': 'Your review has been submitted successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def show_all_reviews(request, id):
    # Get all variations of the product
    product=Product.objects.get(id=id)
    
    return render(request, "Store/Reviews.html", {'product': product})
def fetch_all_reviews(request, id):
    # Get all variations of the product
    variations = Variation.objects.filter(product_id=id)
    
    # Get reviews for all variations
    reviews = RatingReview.objects.filter(product__in=variations)

    # Serialize reviews
    reviews_data = [
        {
            'user_profile_image': review.user.User_Profile_Pic.url,
            'date': review.created_at.strftime('%B %d, %Y'),  # Format date as needed
            'name': review.user.username,
            'rating': review.rating,
            'text': review.review,
        }
        for review in reviews
    ]
    
    return JsonResponse({'reviews': reviews_data})

def fetch_reviews(request, id):
    # Get all variations of the product
    variations = Variation.objects.filter(product_id=id)
    
    # Get top 4 highest-rated reviews for all variations
    reviews = RatingReview.objects.select_related('user').filter(product__in=variations).order_by('-rating')[:4]
    
    # Serialize reviews
    review_list = [
        {
            'user_profile_image': review.user.User_Profile_Pic.url,
            'date': review.created_at.strftime('%B %d, %Y'),  # Format date as needed
            'name': review.user.username,
            'rating': review.rating,
            'text': review.review,
        }
        for review in reviews
    ]
    
    # Get the total count of reviews for the variations
    total_reviews = RatingReview.objects.filter(product__in=variations).count()
    
    return JsonResponse({'reviews': review_list, 'total_reviews': total_reviews})

def review_page(request,id):
    variation=Variation.objects.get(id=id)
    reviews=RatingReview.objects.filter(product=variation)
    return render(request,'RatingAndReviews.html',{'reviews':reviews})
def chartpage(request):
    return render(request,'chart.html')