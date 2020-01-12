$('.facebook-delete').on('click', function(){
    id= $(this).attr('id');
    postUrl = $('#url_facebook_delete').val();
    $('#'+id).css('background-color','lightGrey');
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    $.post({
        url: postUrl,
        dataType: "json",
        data: { 'id' : id, 'csrfmiddlewaretoken' : csrf_token },
        }).done(function(result) {
            if (result._code == 0 ){
                $('#'+id).remove();
            }
            else{
                $('#'+id).css('background-color','white');
                allert("Error")
            }
    });
});
