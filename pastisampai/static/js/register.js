$(document).ready(function(){
    $('form').submit(function(e){
        e.preventDefault();
        let url = register_page
        $.ajax({
            method: 'POST',
            url: url,
            data: $('form').serialize(),
            success: function(data){
                toastr.success(`${data}. you will be redirect in 1.5 seconds`)
                setTimeout(function(){
                    window.location.replace(account_info)
                },1500)
            },
            error: function(xhr){
                console.log(xhr)
                let data = xhr.responseJSON
                for (let i = 0; i < data.length; i++){
                    toastr.error(data[i])
                }
            }
        })
    });
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
})