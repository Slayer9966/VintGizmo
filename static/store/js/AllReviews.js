document.addEventListener('DOMContentLoaded', function() {
     // Pass the product_id from Django template

    function renderStars(rating) {
        let stars = '';
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star text-warning"></i>';
        }
        
        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt text-warning"></i>';
        }
        
        for (let i = fullStars + (hasHalfStar ? 1 : 0); i < 5; i++) {
            stars += '<i class="far fa-star text-warning"></i>';
        }
        
        return stars;
    }

    function fetchReviews() {
        fetch(Review, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const reviewsContainer = document.getElementById('nav-mission');
            reviewsContainer.innerHTML = ''; // Clear existing reviews
    
            data.reviews.forEach(review => {
                const reviewElement = document.createElement('div');
                reviewElement.classList.add('d-flex');
                reviewElement.innerHTML = `
   <div class="review-container">
    <img src="${review.user_profile_image}" class="img-fluid rounded-circle p-3" style="width: 100px; height: 100px;" alt="Reviewer Image">
    <div class="review-text">
        <p class="date-text">${review.date}</p>
        <div class="review-title">
            <h5>${review.name}</h5>
            <div class="review-stars">
                ${renderStars(review.rating)}
            </div>
        </div>
        <p class="text-dark review-content">${review.text}</p>
    </div>
</div>

                `;
                reviewsContainer.appendChild(reviewElement);
            });
           
        })
        .catch(error => console.error('Error fetching reviews:', error));
    }
    fetchReviews()
});