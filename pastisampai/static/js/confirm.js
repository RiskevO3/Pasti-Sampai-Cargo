$(document).ready(function() {
    $('form').submit(function (e) {
        e.preventDefault(); 
        let url = page; // send the form data here.
        $.ajax({
            type: "POST",
            url: url,
            data: $('form').serialize() + `&no_resi=${(no_resi)}`, // serializes the form's elements.
            success: function (data) {
                toastr.success(data)
                setTimeout(function(){
                    window.location.replace('/admin_dashboard')
                },1000)
            },
            error: function(xhr){
                data = xhr.responseJSON
                for (let i = 0; i < data.length; i++){
                    toastr.error(data[i])
                }
            }
        });
        // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});