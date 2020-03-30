$('.register-user').on('click', function(){
    var formData = new FormData();
    username = $('#username').val();
    formData.append('username', username);
    if(username =='' || username.length < 2 && username.length > 256){
        $('#username').attr('class', 'form-control is-invalid');
        return false;
    }

    first_name = $('#first_name').val();
    formData.append('first_name', first_name);
    if(first_name =='' || first_name.length < 2 && first_name.length > 256){
        $('#first_name').attr('class', 'form-control is-invalid');
        return false;
    }

    last_name = $('#last_name').val();
    formData.append('last_name', last_name);
    if(last_name =='' || last_name.length < 2 && last_name.length > 256){
        $('#last_name').attr('class', 'form-control is-invalid');
        return false;
    }

    email = $('#email').val();
    formData.append('email', email);

    password = $('#password').val();
    formData.append('password', password);
    if(password ==''){
        $('#password').attr('class', 'form-control is-invalid');
        return false;
    }

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#url_register').val();
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    window.location.replace('/login');
                    }
                else{
                    $('#error').text(result._error);
                    $('.register-user').text("Error! Click again")
                    function say() {
                      $('.register-user').text("Зареєструватися")
                    }
                    setTimeout(say, 3000);
                    }
        });
});
