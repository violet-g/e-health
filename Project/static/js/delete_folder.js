$(document).ready(function(){
    $("#delete_folder").click(function(){
        var folder_object=$(".active.folder");
        var folder = $.trim($(".active.folder").text());
        
        if(folder=="") //no selected folder => do nothing
        {
            return;
        }

        var delete_button = "<button id='delete' type='button' class='btn btn-primary btn-danger'>Delete</button>"
        
        $("#modal_header").append("<h4 id='added_title'> Are you sure you want to delete this folder?</h4>");
        // $("#modal_body").append("<ul class='nav nav-pills' role='tablist'><li id='added_body' class='active' role='presentation'><a href='#'>" + folder + "</a></li></ul>");
        $("#modal_body").append("<ul class='nav nav-pills' role='tablist'><li id='added_body' class='active' role='presentation'><a href='#'>" + folder + "</a></li></ul>");
        $("#modal_close_button").after($(delete_button));
        $("#myModal").modal('show');
        
        //click event on the delete button on the modal
        $("#delete").click(function(){
            $.ajax({
                url : '/ehealth/delete_folder_ajax/', // the endpoint,commonly same url
                type : "POST", // http method
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                        folder:folder
                    }, // data sent with the post request
        
                // handle a successful response
                success : function(data) {
                    
                    folder_object.next(".privacy_button").remove(); //delete the next privacy button(public/hidden when in profile)
                    folder_object.remove(); //delete the folder itself
                    $("#myModal").modal('hide');
                    $("#header").before("<div class='alert alert-warning mtb20 col-md-8' role='alert'>Folder was deleted!</div>");
                    $(".alert").fadeOut(1750, function(){$(this).remove()});    // fade the created alert
                    $('.folder_choice:contains(' + folder + ')').remove();      //delet the choice in Add to folder
                    
                },
                
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        });
    });
})