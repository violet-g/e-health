
// $(".folder").dblclick(function(){
$("body").on('dblclick', ".folder",function(){
    var folder = $(this).text();    //get the name of the folder
    
    var split_url = window.location.pathname.split("/");
    var user=split_url.indexOf("profile");  //viewd user
    if(user!=-1)
        user = split_url[split_url.indexOf("profile")+1]
    else
        user=""
        
    $.ajax({
        url : '/ehealth/checkout_folder_ajax/', // the endpoint,commonly same url
        type : "POST", // http method
        data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                folder:folder,
                user:split_url[split_url.indexOf("profile")+1],
            }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            
            // Check if this is the right user
            var logged_user = $.trim($('#current-user').attr('user'));
            
            //On success show the data posted to server as a message
            $("#modal_header").append("<h4 id='added_title'>" + folder + "</h4>");
            
            // if there are resulting pages
            if(data['pages'])
            {
                var link_a,title_h4,summary_p,source_p,search_result;
                var pages = data["pages"]
                
                var delete_page = "<button type='button' class='btn btn-primary btn-danger mtb20 delete_page_button'>Delete</button>"
                
                //remove delete button if user is not logged in and viewing offline
                if(user!=logged_user)
                    delete_page="";
                    
                for(var p in pages)
                {
                    // console.log(pages[p]);
                    // console.log(pages[p]['url']);
                    // console.log(pages[p]['summary']);
                    // console.log(pages[p]['source']);
                    // $("#modal_body").append("<p>" + "</p>");
                    var cont = "<div class='row'>";
                    
                    link_a = "<a  id='link' href='#' target='_blank' class='list-group-item table table-responsive '>";
                    title_h4= "<h4 id='title' class='list-group-item-heading mtb15'>";
                    
                    summary_p = "<p id='summary' class='list-group-item-text mtb10'>";
                    source_p = "<p id='source' class='list-group-item-text mtb10'>";
                    
                    link_a = link_a.replace("#",pages[p]['url']);
                    title_h4 += pages[p]['title'] + "</h4>";
                    summary_p += pages[p]['summary'].slice(0,300) + "</p>";
                    source_p += "Source: " + (pages[p]['source']) + "</p>";
                    link_a += title_h4 + summary_p + source_p + "</a>";
                    var scores = "<div class='mtb20'>" +
                        "<div class='scores'> Read: " + parseInt($.trim(pages[p]['readability_score'])) + " </div>" + " " +
                        "<div class='scores'> Subj: " + parseInt($.trim(pages[p]['subjectivity_score'])) + "</div>" + " " + 
                        "<div class='scores'> Sens: " + parseInt($.trim(pages[p]['sentiment_score'])) + "</div>" + "</div>"
                    cont+= "<div class='col-md-10 mtb20 pull-left'>" + link_a+"</div>" + delete_page + scores + "</div>";
                    
                    $("#modal_body").append(cont);
                    
                    $(".delete_page_button").click(function(){
                        //the link has the class pull-left so it was unnecessary to have aditional one
                        var link = $(this).parent().children(".pull-left").children("a").attr("href");
                        var row = $(this).parent(); //by putting the row in a var it will be easier to remove it later
                        
                        var folder = $("#added_title").text();
                        
                        //ajax to delete pages
                        $.ajax({
                                url : '/ehealth/delete_page_ajax/', // the endpoint,commonly same url
                                type : "POST", // http method
                                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                                        folder:folder,
                                        link:link,
                                        }, // data sent with the post request
    
                                // handle a successful response
                                success : function(data) {

                                    row.remove();

                                },
                                // handle a non-successful response
                                error : function(xhr,errmsg,err) {
                                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                }
                        })
                    })
                }
                
                
            }
            $("#myModal").modal('show');
            
        },
        
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});