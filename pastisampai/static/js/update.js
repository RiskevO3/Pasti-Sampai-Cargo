function cekResi(){
    resi = parseInt(document.getElementById('resi').value)
    let url = cekResiPage; // send the form data here.
    submitform = document.getElementById('submitform')
        $.ajax({
            type: "POST",
            url: url,
            data: {'resi':resi},
            success: function (data) {
                submitform.disabled = false
                $("#submitform").attr('class', 'button-update mt-3');
                toastr.success(data)// display the returned data in the console.
            },
            error: function(xhr){
                let data = xhr.responseText
                $("#submitform").attr('class', 'button-update-disabled mt-3');
                submitform.disabled = true
                toastr.error(data)


            }
        });
}
$(document).ready(function() {
    $('form').submit(function (e) {
        let url = page; // send the form data here.
        $.ajax({
            type: "POST",
            url: url,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                document.getElementById("form").reset();
                toastr.success(data)
            },
            error: function(xhr){
                data = xhr.responseJSON
                for (let i = 0; i < data.length; i++){
                    toastr.error(data[i])
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
    });
});