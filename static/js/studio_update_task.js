$('.updtaskpost').on('click', function(){
    var formData = new FormData();
    formData.append('file', $('#exampleInputFile')[0].files[0]);
    title = $('#title').val();
    formData.append('title', title);
    text = $('#text').val();
    formData.append('text', text);
    date_posting = $('#example-datetime-local-input').val();
    formData.append('date_posting', date_posting);
    telegram = $('#id_file_id_t').val();
    formData.append('telegram', telegram);
    facebook = $('#id_file_id_f').val();
    formData.append('facebook', facebook);
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#url_update_task').val();
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            mimeType: "multipart/form-data",
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    window.location.replace("/studio/tasks");
                    }
                else{
                    $('.updtaskpost').text("Error! Click again")
                    }
        });
});
