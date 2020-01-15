$('.save-profile').on('click', function(){
    $('#progress').show();
    $('#progress').attr("class", "spinner-border spinner-border-sm")
    var formData = new FormData();
    formData.append('file', $('#icon')[0].files[0]);
    first_name = $('#first_name').val();
    formData.append('first_name', first_name);
    last_name = $('#last_name').val();
    formData.append('last_name', last_name);
    account_email = $('#account_email').val();
    formData.append('account_email', account_email);
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#url').val();
    console.log(formData);
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            mimeType: "multipart/form-data",
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    $('#progress').attr("class", "fi fi-check")
                    location.reload();
                    }
                else{
                    $('#progress').attr("class", "fi fi-check")
                    $('.save-profile').text("Error! Click again")
                    }
        });
});
