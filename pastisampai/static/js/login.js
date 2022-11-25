$(document).ready(function(e){
    console.log(Boolean(document.getElementById('nexturl').value))
    $('form').submit(function(e){
        e.preventDefault();
        let url = login_page
        let submit = document.getElementById('submit')
        $.ajax({
            method:'POST',
            url:url,
            data: $('form').serialize(),
            success: function(data){
                toastr.success(`${data}. you will be redirect on 1.5 second`)
                submit.className = 'button-login-disabled mt-3'
                submit.disabled = true
                let nextUrl = document.getElementById('nexturl').value
                console.log()
                setTimeout(function(){
                    if (nextUrl){
                        window.location.replace(nextUrl)
                    }else{
                        window.location.replace(account_info)
                    }
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