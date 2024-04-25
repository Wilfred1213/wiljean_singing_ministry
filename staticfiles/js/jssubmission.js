$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        // Serialize form data
        var formData = new FormData($(this)[0]);
        // let url1 = "{% url 'index' %}"
        // Submit form data using AJAX
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if(response.success){
                // Handle successful response
                console.log(response.message)
                $('#notification_message').html(`<div class="alert alert-success">${response.message}</div>`);
                // Optionally, you can reset the form
                $('#uploadForm')[0].reset();
                // window.location.href = "{% url 'index' %}"

                }else{
                console.log(response.message)
                // Handle successful response
                $('#notification_message').html(`<div class="alert alert-success">${response.message}</div>`);
                // Optionally, you can reset the form
                $('#uploadForm')[0].reset();
                }
                
            },
            error: function(xhr, errmsg, err) {
                // Handle error
                $('#notification_message').html('<div class="alert alert-danger">Error: ' + errmsg + '</div>');
            }
        });
    });

      
        
});
