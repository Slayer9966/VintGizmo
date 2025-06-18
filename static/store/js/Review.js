document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
fetchReviews()
    stars.forEach(star => {
        star.addEventListener('mouseover', function () {
            const value = this.getAttribute('data-value');
            highlightStars(value);
        });

        star.addEventListener('mouseout', function () {
            const value = ratingInput.value;
            highlightStars(value);
        });

        star.addEventListener('click', function () {
            const value = this.getAttribute('data-value');
            ratingInput.value = value;
            highlightStars(value);
        });
    });

    function highlightStars(value) {
        stars.forEach(star => {
            if (star.getAttribute('data-value') <= value) {
                star.classList.add('text-warning');
            } else {
                star.classList.remove('text-warning');
            }
        });
    }
    $('#review-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = $(this).serialize(); // Serialize form data

        $.ajax({
            url: submitReviewUrl,
            type: "POST",
            data: formData,
            success: function(response) {

                if (response.status === 'success') {
                    $('#review-message').html('<p class="text-success">' + response.message + '</p>');
                    $('#review-form')[0].reset(); // Clear the form
                    fetchReviews()
                } else {
                    $('#review-message').html('<p class="text-danger">' + response.message + '</p>');
                }
                console.log(response)
            },
            error: function(xhr, status, error) {
                $('#review-message').html('<p class="text-danger">An error occurred while submitting your review.</p>');
            }
        });
    });
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
            if (data.total_reviews > 3) {
                const seeAllButton = document.createElement('button');
                seeAllButton.id = 'see-all-button';
                seeAllButton.type = 'button';
                seeAllButton.className = 'btn border border-secondary text-primary rounded-pill px-4 py-3';
                seeAllButton.textContent = 'See All';
                seeAllButton.dataset.url = `/show-all-reviews/${Product_id}/`;
 console.log(Product_id)
                
                reviewsContainer.appendChild(seeAllButton);
            }
        })
        .catch(error => console.error('Error fetching reviews:', error));
    }

});
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('nav-mission').addEventListener('click', function(event) {
        if (event.target && event.target.id === 'see-all-button') {
            const url = event.target.dataset.url; // Retrieve the URL from the data attribute
            if (url) {
                window.location.href = url; // Navigate to the URL
            }
        }
    });
});
