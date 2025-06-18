$(document).ready(function() {
    var searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            var input = this.value.toLowerCase();
            var tableRows = Array.from(document.querySelectorAll("#tableBody tr"));

            tableRows.forEach(function (row) {
                var rowText = row.textContent.toLowerCase();
                if (rowText.includes(input)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    }
    $('.update').on('click', function() {
        var orderId = $(this).data('id');  // Get the order ID from data-id attribute
        console.log("Clicked update with order ID:", orderId);  // Debug log
       
        $.ajax({
            url: '/get-order-id/',  // URL to the Django view
            type: 'GET',            // or 'POST' depending on your need
            data: {
                order_id: orderId   // Send the order ID to the backend
            },
           
            success: function(response) {
                console.log('Response received:', response);  // Debug log
                $('#order_id').val(response.order_id);  // Populate input field
                $('#ChangeModal').modal("show");
            },
            error: function(xhr, status, error) {
                console.error('Error fetching order ID:', error);  // Error handling
            }
        });
    });

    $('.del').on('click', function() {
        $('#ChangeModal').modal("hide");  // Hide the modal
    });
});
