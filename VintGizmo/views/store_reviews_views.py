from django.shortcuts import render, get_object_or_404, redirect
from ..models.store_review import StoreReview
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test

def create_review_ajax(request):
    if request.method == 'POST':
        # Create a new StoreReview object with data from the form
        name = request.POST.get('name')
        profession = request.POST.get('profession')
        review = request.POST.get('review')
        image = request.FILES.get('image')
        
        # Save the review
        try:
            StoreReview.objects.create(
                name=name,
                profession=profession,
                review=review,
                image=image
            )
            return JsonResponse({
                'success': True,
                'message': 'Your review was submitted successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })
# Create a new review
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def create_review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        profession = request.POST.get('profession')
        review = request.POST.get('review')
        image = request.FILES.get('image')

        StoreReview.objects.create(name=name, profession=profession, review=review, image=image)
        
        messages.success(request, "Review created successfully.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@user_passes_test(is_superuser)
def update_review(request):
    review_id = request.POST.get('review_id')
    review = get_object_or_404(StoreReview, id=review_id)
    
    if request.method == 'POST':
        review.name = request.POST.get('name')
        review.profession = request.POST.get('profession')
        review.review = request.POST.get('review')
        review.status = request.POST.get('status')
        
        if 'image' in request.FILES:
            review.image = request.FILES['image']
        
        review.save()
        
        messages.success(request, "Review updated successfully.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@user_passes_test(is_superuser)
def delete_review(request, review_id):
    review = get_object_or_404(StoreReview, id=review_id)
    
    try:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    except Exception as e:
        messages.error(request, f"Failed to delete review: {str(e)}")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@user_passes_test(is_superuser)
def pending_reviews(request):
    reviews = []
    try:
        reviews = StoreReview.objects.filter(status='pending')
    except Exception as e:
        messages.error(request, f"Error getting pending reviews: {str(e)}")
    return render(request, "PendingStoreReview.html", {'reviews': reviews})

@login_required
@user_passes_test(is_superuser)
def approved_reviews(request):
    reviews = []
    try:
        reviews = StoreReview.objects.filter(status='approved')
    except Exception as e:
        messages.error(request, f"Error getting approved reviews: {str(e)}")
    return render(request, "ApprovedStoreReview.html", {'reviews': reviews})

@login_required
@user_passes_test(is_superuser)
def rejected_reviews(request):
    reviews = []
    try:
        reviews = StoreReview.objects.filter(status='rejected')
    except Exception as e:
        messages.error(request, f"Error getting rejected reviews: {str(e)}")
    return render(request, "RejectedStoreReview.html", {'reviews': reviews})
