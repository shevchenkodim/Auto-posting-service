$('.login-user').on('click', function(){
    var formData = new FormData();
    username = $('#username').val();
    formData.append('username', username);
    if(username ==''){
        $('#username').attr('class', 'form-control is-invalid');
        return false;
    }

    password = $('#password').val();
    formData.append('password', password);
    if(password ==''){
        $('#password').attr('class', 'form-control is-invalid');
        return false;
    }

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#url_login').val();
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    window.location.replace('/studio/');
                    }
                else{
                    $('#error').text(result._error);
                    $('.login-user').text("Error! Click again")
                    function say() {
                      $('.login-user').text("Зареєструватися")
                    }
                    setTimeout(say, 3000);
                    }
        });
});
