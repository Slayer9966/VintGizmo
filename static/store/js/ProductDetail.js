document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('quantity');
    if (inputField.value === '' || inputField.value === null) {
        inputField.value = 1;
    }
    document.querySelectorAll('.variation-item').forEach(item => {
        item.addEventListener('click', function() {
            const variationId = this.id.split('-')[1];
            fetch(`/variation/${variationId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error:', data.error);
                        return;
                    }
    
                    // Update the carousel with the new images
                    document.querySelector('#carouselId .carousel-inner').innerHTML = data.images.map((img, index) =>
                        `<div class="carousel-item ${index === 0 ? 'active' : ''} rounded">
                            <img src="${img.url}" class="img-fluid w-100 h-100 bg-secondary rounded" alt="Variation image">
                        </div>`
                    ).join('');
    
                    // Update the product details with the new variation details
                    document.querySelector('#product-name').textContent = `Variation: ${data.name}`;
                    document.querySelector('#product-price').textContent = `Rs.${data.sales_price}`;
                    document.querySelector('#product-description').textContent = data.description;
                    document.querySelector('#variation_id').value = data.id;
                    console.log(data.average_rating)
                    // Update the average rating stars
                    const stars = document.querySelector('.d-flex.mb-4');
                    stars.innerHTML = '';
                    for (let i = 1; i <= 5; i++) {
                        const starClass = i <= data.average_rating ? 'text-warning' : 'star1';
                        stars.innerHTML += `<i class="fa fa-star ${starClass}"></i>`;
                    }
                    document.querySelector('#variation').value = data.id;

                })
                .catch(error => console.error('Error:', error));
        });
    });
    
    function addToCart(productId, variationId, quantity) {
        console.log(variationId)
        fetch(`/add-to-cart/${productId}/${variationId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'), // Fetch CSRF token
            },
            body: new URLSearchParams({
                'quantity': quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showModal(data.message); // Show the response in the modal
                const cartQuantitySpan = document.getElementById('cart_quantity');

// Convert the current text and quantity to numbers
                const currentValue = parseFloat(cartQuantitySpan.textContent) || 0;
                const quantityToAdd = parseFloat(quantity) || 0;

                // Update the content
                cartQuantitySpan.textContent = currentValue + quantityToAdd;
                // Optionally update the cart display
            } else {
                showModal(data.message); // Show the response in the modal
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred');
        });
    }

    // Function to get the CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Example usage
    // Replace these values with your actual productId, variationId, and quantity
    
    
    // Add to cart when a button is clicked
    document.getElementById('add-to-cart-button').addEventListener('click', function() {
        const productId = document.getElementById('product_id').value;
        const variationId = document.getElementById('variation_id').value;
        const quantity = document.querySelector('.quantity input').value; // Get the updated quantity
    
        addToCart(productId, variationId, quantity);
    });
    document.querySelectorAll('.quantity button').forEach(button => {
        button.addEventListener('click', function() {
            const inputField = this.closest('.quantity').querySelector('input');
            let oldValue = parseInt(inputField.value, 10);

            // Update value based on button clicked
            let newVal;
            if (this.classList.contains('btn-plus')) {
                newVal = oldValue + 1;
            } else {
                newVal = (oldValue > 1) ? oldValue - 1 : 1;
            }

            // Update the input field value
            inputField.value = newVal;

            // For debugging: Output to console to verify value
            console.log("Updated Quantity: " + newVal);
        });
    });
    function showModal(responseMessage) {
        const messageDiv = document.getElementById("responseMessage");
        messageDiv.innerHTML = responseMessage; // Set the response message inside the modal
      
        // Trigger Bootstrap modal
        const modal = new bootstrap.Modal(document.getElementById('responseModal'));
        modal.show();
      }
      

});