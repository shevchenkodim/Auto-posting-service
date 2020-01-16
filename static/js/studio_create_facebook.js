$('.facebook').on('click', function(){
    $('#progress').show();
    $('#progress').attr("class", "spinner-border spinner-border-sm")
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
                    $('#progress').attr("class", "fi fi-check")
                    location.reload();
                    }
                else{
                    $('#progress').attr("class", "fi fi-check")
                    $('.telegram').text("Error! Click again")
                    }
        });
});
