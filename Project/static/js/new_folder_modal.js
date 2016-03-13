$('#new_folder_modal').on('shown.bs.modal', function(event){
    console.log("shown");
    console.log($("input[name=new_folder_name]").val())
    $("#create").click(function(){
        var fname=$("input[name=new_folder_name]").val();
        console.log(fname)
        $.post('/ehealth/dashboard/new_folder_ajax',
        {
            folder:fname,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },function(data){
            alert('folder created: ' + data);
        });
    });
})