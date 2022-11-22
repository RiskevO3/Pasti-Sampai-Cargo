$(document).ready(function() {
    $('form').submit(function (e) {
        let search_city = document.getElementsByClassName('card-about-output mt-4 overflow-auto')[0]
        search_city.innerHTML = ''
        e.preventDefault(); 
        let url = page; // send the form data here.
        $.ajax({
            type: "POST",
            url: url,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                for (let i = 0; i < data.length; i++){
                    search_city.innerHTML+=(`${i+1}. ${data[i]['address']} | ${data[i]['kabkota_name']} | ${data[i]['cabang_name']} | ${data[i]['kodePos']} <br><br><br>`)
                }
            },
            error: function(xhr){
                data = xhr.responseText
                search_city.innerHTML += data
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