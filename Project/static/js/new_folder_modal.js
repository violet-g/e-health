$('#new_folder_modal').on('shown.bs.modal', function(event){
    console.log("shown");
    console.log($("input[name=new_folder_name]").val())
    var fname=$("input[name=new_folder_name]").val();
    // $("#create").click(function(){
    //     console.log(fname)
    //     $.post('/ehealth/dashboard/new_folder_ajax',
    //     {
    //         folder:fname,
    //         csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
    //     },function(data){
    //         console.log(data);
    //         alert('folder created: ' + data);
    //     });
    // });
    
    $("#create").click(function(){
        $.ajax({
            url : '/ehealth/dashboard/new_folder_ajax', // the endpoint,commonly same url
            type : "POST", // http method
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                    folder:fname
                }, // data sent with the post request
    
            // handle a successful response
            success : function(json) {
                console.log(json); // another sanity check
                //On success show the data posted to server as a message
                alert('Hi   '+json['name']);
            },
            
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
         });
    });
    
    
})