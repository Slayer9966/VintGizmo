document.getElementById('trackButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const orderNumber = document.getElementById('orderNumberInput').value;

    if (orderNumber.trim() === "") {
        alert("Please enter a valid order number.");
        return;
    }

    fetch('/track-order/', { // Adjust the URL to match your endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if using Django
        },
        body: JSON.stringify({ order_number: orderNumber })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response data:', data); // Log response data for debugging
        if (data.success) {
            // Display order details
            const orderDetails = data.order;
            displayOrderDetails(orderDetails);
        } else {
            // Handle error (e.g., order not found)
            document.getElementById('orderDetails').innerHTML = `<p>${data.message}</p>`;
        }
    })
    .catch(error => console.error('Error:', error));
});

function displayOrderDetails(details) {
    console.log('Order details received:', details); // Log details for debugging

    if (!details) {
        document.getElementById('orderDetails').innerHTML = '<p>No order details provided.</p>';
        return;
    }

    const statusText = details.status ? (details.status.toLowerCase() === 'pending' ? 'Processing' : details.status) : 'Unknown';

    const itemsHTML = details.items && details.items.length > 0
        ? details.items.map(item => `
            <tr>
                <td>${item.product_name || 'N/A'}</td>
                <td>${item.variation_name || 'N/A'}</td>
                <td>${item.quantity || 'N/A'}</td>
                <td>${item.price || 'N/A'}</td>
                <td>${item.total_cost || 'N/A'}</td>
                <td>${item.discounted_price || 'N/A'}</td>
            </tr>
        `).join('')
        : '<tr><td colspan="5">No items found.</td></tr>';

    const orderDetailsHTML = `
        <h3>Order Details</h3>
        <p><strong>Order Number:</strong> ${details.order_number || 'N/A'}</p>
        <p><strong>Discount :</strong> ${details.discount || 'N/A'}</p>
        <p><strong>Status:</strong> ${statusText}</p>
        <h4>Items:</h4>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Variation Name</th>
                    <th>Quantity</th>
                    <th>Price Per Item</th>
                    <th>Total Cost</th>
                    <th>Discounted Cost</th>

                </tr>
            </thead>
            <tbody>
                ${itemsHTML}
            </tbody>
        </table>
    `;

    document.getElementById('orderDetails').innerHTML = orderDetailsHTML;
}

// Utility function to get CSRF token if using Django
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
