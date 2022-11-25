$(document).ready(function(){
    $('#logout').click(function(){
        let url = '/logout'
        $.ajax({
            method:'POST',
            url:url,
            success:function(data){
                toastr.info(data['messages'])
                document.getElementById('logout').disabled = true
                setTimeout(function(){
                    window.location.replace(data['url'])
                },1500)
            },
            error:function(xhr){
                console.log(xhr)
            }
        })
    })
})