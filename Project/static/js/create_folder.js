$(document).ready(function(){
    $("#create_folder").click(function(){
        // var folder_object=$(".active.folder");
        // var folder = $.trim($(".active.folder").text());
        // if(folder=="")
        // {
        //     console.log(folder);
        //     return;
        // }
        // console.log(folder);
        var create_button = "<button id='create' type='button' class='btn btn-primary btn-success'>Create</button>"
        console.log("click");
        $("#modal_header").append("<h4 id='added_title'> Create new folder </h4>");
        // $("#modal_body").append("<ul class='nav nav-pills' role='tablist'><li id='added_body' class='active' role='presentation'><a href='#'>" + folder + "</a></li></ul>");
        $("#modal_body").append("<input type='folder' class='form-control' id='new_folder_name' name='new_folder_name' placeholder='Folder name'>");
        $("#modal_close_button").after($(create_button));
        $("#myModal").modal('show');
        
        $("#new_folder_name").focus();
        $("#new_folder_name").keypress(function(event){
            if (event.which == 13) {    //enter button
                $("#create").trigger('click');
            }
        });
        
        $("#create").click(function(){
            $(".alert").remove(); //delete any alerts from before
            var fname=$.trim($("input[name=new_folder_name]").val());
            $("input[name=new_folder_name]").val('');
            if(fname=="")
            {
                $("#new_folder_name").before("<div class='alert alert-danger' role='alert'>Nameless folder?</div>");
                return;
            }
            
            
            $.ajax({
                url : '/ehealth/new_folder_ajax/', // the endpoint,commonly same url
                type : "POST", // http method
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                        folder:fname
                    }, // data sent with the post request
        
                // handle a successful response
                success : function(data) {
                    console.log(data); // another sanity check
                    //On success show the data posted to server as a message
                    // alert('Hi   '+data['name']);
                    if(data['repeat']==true)
                    {
                        $("#new_folder_name").before("<div class='alert alert-danger ' role='alert'>You already have a folder with that name!</div>");
                        return;
                    }
                    else
                    {
                        $("#header").before("<div class='alert alert-success mtb20 col-md-8' role='alert'>Folder was created!</div>");
                        $(".alert").fadeOut(1750, function(){$(this).remove()});
                    }
                    $("#myModal").modal('hide');
                    if(window.location.pathname.indexOf("profile") == -1)
                    {
                        var new_folder = "<li role='presentation' class='btn-block folder'><a class='nofocus' href='#!' >" +
                                        fname +
                                        "</a></li>"
                        // location.reload();
                        // $('#new_folder_modal').modal('hide');
                        console.log(new_folder);
                        console.log($("#folder_list").children());
                        $(".folder_list").append(new_folder);
                        var new_folder_choice = "<li class='folder_choice'><a href='#!'>" + fname + "</a></li>"
                        $(".folder_options").append(new_folder_choice);
                    }
                    else
                    {
                        var new_folder = "<li role='presentation' class='folder col-md-9 pull-left'><a class='nofocus' href='#!' >" + fname + "</a></li>";
                        var new_privacy_button = "<button type='button' class='btn btn-success col-md-3 pull-right mt3 privacy_button text-justify'> Hidden </button>";
                        $("#save_folder_changes").before(new_folder);
                        $("#save_folder_changes").before(new_privacy_button);
                    }
                },
                
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        });
    });
})