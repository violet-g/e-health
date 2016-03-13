$('#myModal').on('show.bs.modal', function(event){
    $("#create").click(function(){
        var fname=$("input").val();
        $.post('/ehealth/dashboard/new_folder_ajax',
        {
            folder:fname
        },function(data){
            alert('folder created: ' + fname);
        });
    });
})