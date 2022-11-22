$(document).ready(function(){
    $('form').submit(function(e){
        e.preventDefault();
        let url = login_page
        $.ajax({
            method:'POST',
            url:url,
            data: $('form').serialize(),
            success: function(data){
                toastr.success(`${data}. you will be redirect on 1.5 second`)
                setTimeout(function(){
                    window.location.replace(account_info)
                },1500)
            },
            error: function(xhr){
                data = xhr.responseText
                toastr.error(data)
            }
        });
    });
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    });
});