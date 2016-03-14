$(document).ready(function(){
    $("#delete_folder").click(function(){
        var folder = $.trim($(".active.folder").text());
        if(folder=="")
        {
            console.log(folder);
            return;
        }
        console.log(folder);
        $("#modal_header").append("<h4 id='added_title'> Are you sure you want to delete this folder?</h4>");
        // $("#modal_body").append("<ul class='nav nav-pills' role='tablist'><li id='added_body' class='active' role='presentation'><a href='#'>" + folder + "</a></li></ul>");
        $("#modal_body").append("<ul class='nav nav-pills' role='tablist'><li id='added_body' class='active' role='presentation'><a href='#'>" + folder + "</a></li></ul>");
        $("#myModal").modal('show');
        $("#delete").click(function(){
            $.ajax({
                url : '/ehealth/delete_folder_ajax/', // the endpoint,commonly same url
                type : "POST", // http method
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                        folder:folder
                    }, // data sent with the post request
        
                // handle a successful response
                success : function(data) {
                    console.log(data); // another sanity check
                    //On success show the data posted to server as a message
                    location.reload();
                },
                
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        });
        //on hide remove the added element to the modal, since we dont need it anymore
        $('#myModal').on('hide.bs.modal',function(){
            $("#added_title").remove();
            $("#added_body").remove();
        });
    });
})