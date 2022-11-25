$(document).ready(function() {
    $('form').submit(function (e) {
        let url = page; // send the form data here.
        $.ajax({
            type: "POST",
            url: url,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                trackingresult = document.getElementById('trackingresult')
                if (data != 'noresi tidak ada!'){
                    document.getElementById("form").reset();
                    trackingresult.innerHTML = `${data['arrived_at']} | ${data['time_on_update']}`  // display the returned data in the console.
                }
                else {
                    document.getElementById("form").reset();
                    trackingresult.innerHTML = data
                }
            }
        });
        e.preventDefault(); // block the traditional submission of the form.
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