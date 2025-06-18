function resendOtp() {
    $.ajax({
        url: resendOtpUrl,  // URL to send the request to
        type: "POST",
        dataType: "json",
        headers: {
            'X-CSRFToken': csrfToken// Django CSRF token
        },
        data: {},  // Send any necessary data here if needed
        success: function(response) {
            if (response.status === 200) { // Assuming 200 is the success status code
                alert('OTP resent successfully: ' + response.message);
            } else {
                alert('Error: ' + response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred while resending OTP.');
        }
    });
}
