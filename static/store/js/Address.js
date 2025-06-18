document.addEventListener('DOMContentLoaded', function() {
    $('.addAddress').on('click', function() {
        $('#exampleModal').modal('show');
    });
    $('.close_add').on('click', function() {
        $('#exampleModal').modal('hide');
    });
    $('.update-address').on('click', function() {
        var addressId = $(this).data('id');
        
        $.ajax({
            url: `/addresses/${addressId}/`, // Adjust URL to your address detail view
            method: 'GET',
            success: function(data) {
                // Populate the modal fields with address data
                $('#address_id').val(data.id);
                $('#name').val(data.name);
                $('#phone_number').val(data.phone_number);
                $('#street_address').val(data.street_address);
                $('#city').val(data.city);
                $('#state').val(data.state);
                $('#postal_code').val(data.postal_code);
                
                // Show the modal
                $('#exampleModalUpdate').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Error fetching address data:', error);
            }
        });
    });
    
});
