document.addEventListener('DOMContentLoaded', function() {
    let subtotal = 0;

    // Function to update cart item quantity via AJAX
    function updateCartItemQuantity(id, change, flag) {
        const url = `/update-cart-item/${id}/`;
        const quantityInput = document.querySelector(`#cart-item-${id} input[type='text']`);
        let newQuantity = 0;
        const cartQuantitySpan = document.querySelector('#cart_quantity');

        if (!flag) {
            newQuantity = parseInt(quantityInput.value, 10) + change;
        } else {
            newQuantity = change;
        }

        if (newQuantity > 0) {
            const requestBody = new URLSearchParams();
            requestBody.append('quantity', newQuantity);

            fetch(url, {
                method: 'POST',
                body: requestBody,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success === true) {
                    quantityInput.value = newQuantity;
                    updateTotalPrice(quantityInput.closest('tr'), newQuantity);
                    if (cartQuantitySpan && !flag) {
                        const currentCartQuantity = parseInt(cartQuantitySpan.textContent, 10) || 0;
                        cartQuantitySpan.textContent = currentCartQuantity + change;
                    } else {
                        cartQuantitySpan.textContent = change;
                    }
                    updateShippingCost(); // Call to recalculate shipping cost

                } else {
                    showModal('Failed to update cart item: ' + (data.error || 'No error message provided'));
                }

            })
            .catch(error => {
                console.error('Fetch error:', error);
                showModal('An error occurred while updating the cart item.');
            });
        }
    }
    function updateShippingCost() {
        let totalShippingCost = 0;

        // Iterate through each item row to calculate total shipping cost
        document.querySelectorAll('tr[id^="cart-item-"]').forEach(row => {
            const shippingCostInput = row.querySelector('.item-shipping-cost');
            const quantityInput = row.querySelector('.item-quantity');

            if (shippingCostInput && quantityInput) {
                const shippingCost = parseFloat(shippingCostInput.value.trim()) || 0;
                const quantity = parseInt(quantityInput.value, 10) || 0;
                totalShippingCost += (shippingCost * quantity);
            }
        });

        // Update shipping cost display
        document.getElementById('shipping_cost').value = totalShippingCost;
        document.getElementById('displayShippingCost').textContent = `$${totalShippingCost}`;
        updateTotalAmount(); // Update total amount after changing shipping cost
    }

    // Function to update the total price in the table
    function updateTotalPrice(row, newQuantity) {
        const salesPriceElement = row.querySelector('td:nth-child(5) p');
        const totalPriceElement = row.querySelector('td:nth-child(7) p');
    
        if (!salesPriceElement || !totalPriceElement) {
            console.error('Sales price or total price element not found.');
            return;
        }
    
        const salesPriceText = salesPriceElement.textContent.trim();
        const salesPrice = parseFloat(salesPriceText.replace('$', '').trim());
        if (isNaN(salesPrice)) {
            console.error('Invalid sales price:', salesPriceText);
            return;
        }
    
        const totalPrice = salesPrice * newQuantity;
        totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
        updateSubtotal();
    }

    function updateSubtotal() {
        subtotal = 0; // Reset subtotal
        document.querySelectorAll('tr[id^="cart-item-"]').forEach(row => {
            const totalPriceText = row.querySelector('td:nth-child(7) p').textContent.trim();
            const totalPrice = parseFloat(totalPriceText.replace('$', '').trim());
            if (!isNaN(totalPrice)) {
                subtotal += totalPrice;
            }
        });
        document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
        updateTotalAmount(); // Update total amount whenever subtotal changes
    }

    function updateTotalAmount() {
        const discountPercentage = parseFloat(document.getElementById('couponMessage').dataset.discount) || 0;
        const shipping = parseFloat(document.getElementById('shipping_cost').value);
        // Calculate the discount amount
        const discountAmount = (subtotal * discountPercentage) / 100;

        // Calculate total amount
        const totalAmount = subtotal - discountAmount + shipping;
        document.getElementById('totalAmount').textContent = `$${totalAmount.toFixed(2)}`;
    }

    // Function to delete a cart item via AJAX
    $(document).on('click', '.delete-cart-item-button', function() {
        const shippingCost = parseFloat($(this).data('ship')) || 0;
        const cartItemId = $(this).data('cartItemId');
        
        $.ajax({
            url: `/delete-cart-item/${cartItemId}/`,
            type: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            success: function(data) {
                if (data.success) {
                    $(`#cart-item-${cartItemId}`).remove();
                    const currentShipping = parseFloat($('#shipping_cost').val()) || 0;
                    const updatedShipping = currentShipping - shippingCost;
                    $('#shipping_cost').val(updatedShipping);
    
                    $('#displayShippingCost').text(`$${updatedShipping.toFixed(2)}`);
                    const quantity = data.quantity || 0;
                    const currentQuantity = parseInt($('#cart_quantity').text()) || 0;
                    const updatedQuantity = currentQuantity - quantity;
                    $('#cart_quantity').text(updatedQuantity);
                    showModal('Item deleted successfully!');
                    updateSubtotal();
                } else {
                    showModal('Failed to delete item.');
                }
            },
            error: function(error) {
                console.error('Error:', error);
                showModal('An error occurred while deleting the item.');
            }
        });
    });
    
    // Utility function to show modal with message
    function showModal(message) {
        const modalMessage = document.getElementById('responseMessage');
        modalMessage.textContent = message;
        $('#responseModal').modal('show');
    }

    // Utility function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; cookies[i]; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Add event listeners for minus and plus buttons
    document.querySelectorAll('.btn-minus').forEach(button => {
        button.addEventListener('click', function() {
            const cartItemId = this.closest('tr').id.replace('cart-item-', '');
            updateCartItemQuantity(cartItemId, -1, false);
        });
    });

    document.querySelectorAll('.btn-plus').forEach(button => {
        button.addEventListener('click', function() {
            const cartItemId = this.closest('tr').id.replace('cart-item-', '');
            updateCartItemQuantity(cartItemId, 1, false);
        });
    });

    // Handle direct input change
    document.querySelectorAll('input[data-cart-item-id]').forEach(inputField => {
        inputField.addEventListener('change', function() {
            const newQuantity = parseInt(this.value, 10);
            const cartItemId = this.dataset.cartItemId;
            if (newQuantity > 0) {
                updateCartItemQuantity(cartItemId, newQuantity, true);
            } else {
                this.value = 1;
                showModal('Quantity must be at least 1.');
            }
        });
    });

    // Handle the checkout button click
    document.getElementById('checkoutButton').addEventListener('click', function() {
        const selectedItems = Array.from(document.querySelectorAll('input[name="selected_items"]:checked'))
                                   .map(checkbox => checkbox.value);
        if (selectedItems.length > 0) {
            fetch('/set-selected-items/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ selected_items: selectedItems })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = checkoutUrl;
                } else {
                    showModal('Failed to save selected items. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showModal('An error occurred. Please try again.');
            });
        } else {
            showModal('Please select at least one item.');
        }
    });

    // Handle the coupon application
    document.getElementById('applyCouponForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const couponCode = document.getElementById('couponCode').value;

        fetch('/apply-coupon/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ coupon_code: couponCode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('couponMessage').textContent = 'Coupon applied successfully!';
                document.getElementById('couponMessage').dataset.discount = data.discount;
                document.getElementById('couponMessage').style.color = 'green';
                updateTotalAmount();
            } else {
                document.getElementById('couponMessage').textContent = data.message || 'Failed to apply coupon.';
                document.getElementById('couponMessage').dataset.discount = 0;
                document.getElementById('couponMessage').style.color = 'red';
                updateTotalAmount();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('An error occurred while applying the coupon.');
        });
    });

    // Trigger subtotal calculation on page load
    updateSubtotal();
});
