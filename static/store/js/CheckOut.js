
    // Update total amount with discount
    function updateTotalAmount() {
        const subtotal = parseFloat(document.getElementById('subtotal').textContent.replace('$', ''));
        const shipping = parseFloat(document.getElementById('shipping').textContent.replace('$', ''));
        const discount = parseFloat(document.getElementById('discountAmount').textContent.replace('$', '')) || 0;

        const total = subtotal + shipping - discount;
        document.getElementById('totalAmount').textContent = `$${total.toFixed(2)}`;
    }

    // Run the function to update total on page load
    updateTotalAmount();
