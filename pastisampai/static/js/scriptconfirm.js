
listUsernameValidator = [false,false]
const checkUsername = (data) => {
    let dataUsername = 0
    if(data[0] == 'username_r'){
        dataUsername = 1
    }
    else{
        dataUsername = 0
    }
    let url = '{{url_for("check_username")}}'
    submitform = document.getElementById('submitform')
    $.ajax({
        type:"POST",
        url:url,
        data:{'username':data[1],'type_username':data[0]},
        success: function(data){
            toastr.success(data)
            listUsernameValidator[dataUsername] = true
        },
        error: function(xhr){
            console.log(xhr)
            data = xhr.responseText
            toastr.error(data)
            $("#submitform").attr('class','button-confirm-disable')
            listUsernameValidator[dataUsername] = true
        }
})
if (listUsernameValidator[0] && listUsernameValidator[1]){
    submitform.disabled = false
    $('#submitform').attr('class','button-confirm')
}
else{
    submitform.disabled = true
    $('#submitform').attr('class','button-confirm-disable')
}
}
