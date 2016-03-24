$(document).ready(function(){
    $("#create_folder").click(function(){
        
        var create_button = "<button id='create' type='button' class='btn btn-primary btn-success'>Create</button>"
        
        $("#modal_header").append("<h4 id='added_title'> Create new folder </h4>");
        
        $("#modal_body").append("<input type='folder' class='form-control' id='new_folder_name' name='new_folder_name' placeholder='Folder name'>");
        $("#modal_close_button").after($(create_button));
        $("#myModal").modal('show');
        
        // $("#new_folder_name").focus(); //this used to work but doesnt now..
        
        //Create folders with enter key too
        $("#new_folder_name").keypress(function(event){
            if (event.which == 13) {    //enter button
                $("#create").trigger('click');
            }
        });
        
        $("#create").click(function(){
            $(".alert").remove(); //delete any alerts from before
            var fname=$.trim($("input[name=new_folder_name]").val());   //get folder name
            
            $("input[name=new_folder_name]").val('');   //set the field to null
            
            if(fname=="")   //if the field was empty(the user clicked create before writing a name) raise a warning
            {
                $("#new_folder_name").before("<div class='alert alert-danger' role='alert'>Nameless folder?</div>");
                return;
            }
            
            $.ajax({
                url : '/ehealth/new_folder_ajax/', // the endpoint,commonly same url
                type : "POST", // http method
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,    //VERY IMPORTANT TO PASS THE CSRF token!!! 
                        folder:fname                                                                        //TOOK ME AN HOUR(at least) TO FIND THAT BUG!!!
                    }, // data sent with the post request
        
                // handle a successful response
                success : function(data) {
                    if(data['repeat']==true)    //is this folder already in the db? Raise an aler and return, so that nothing happens really!
                    {
                        $("#new_folder_name").before("<div class='alert alert-danger ' role='alert'>You already have a folder with that name!</div>");
                        return;
                    }
                    else    //Folder is new. Raise a success alert
                    {
                        $("#header").before("<div class='alert alert-success mtb20 col-md-8' role='alert'>Folder was created!</div>");
                        $(".alert").fadeOut(1750, function(){$(this).remove()});
                    }
                    
                    $(".no_folders").remove(); //remove the "You have no folders text if it's still there"
                    $("#myModal").modal('hide');
                    
                    
                    //Are we on the dashboard or our somebody else's profile? (save_folder_changes is only on out own profile page)
                    if(window.location.pathname.indexOf("profile") == -1 || !$("#save_folder_changes").length)
                    {
                        //dynamically add the folder to the front end as well
                        
                        var new_folder = "<li role='presentation' class='btn-block folder'><a class='nofocus' href='#!' >" +
                                        fname +
                                        "</a></li>"
                                        
                        $(".folder_list").append(new_folder);
                        var new_folder_choice = "<li class='folder_choice'><a href='#!'>" + fname + "</a></li>"
                        $(".folder_options").append(new_folder_choice);
                    }
                    //Else => we are on our own profile page, hence we need a privacy button for the folder and a general save button for folder privacy
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