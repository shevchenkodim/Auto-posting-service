$('.telegram').on('click', function(){
    $('#progress').show();
    $('#progress').attr("class", "spinner-border spinner-border-sm")
    var formData = new FormData();
    name_channel = $('#channel').val();
    if(name_channel =='' || name_channel.length < 2 && name_channel.length > 256){
        alert("Error! Please, check your Name channel");
        $('#progress').attr("class", "fi fi-check")
        return false;
    }
    formData.append('name_channel', name_channel);
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    console.log(formData);
    postUrl = $('#url_telegram').val();
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
