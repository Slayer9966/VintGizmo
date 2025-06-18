
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum
from ..models.products import Product
from ..models.variation import Variation
from django.db.models import Q
from django.db.models.functions import Lower, Replace

def search_home_page(request):
    query = request.GET.get('q')  # Get the search keyword from the request
    products_with_variations = []

    if query:
        # Preprocess the search query: make it lowercase and remove spaces
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