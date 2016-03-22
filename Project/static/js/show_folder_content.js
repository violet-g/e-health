
// $(".folder").dblclick(function(){
$("body").on('dblclick', ".folder",function(){
    var folder = $(this).text();
    // console.log(folder);
    var split_url = window.location.pathname.split("/");
    var user=split_url.indexOf("profile");
    if(user!=-1)
        user = split_url[split_url.indexOf("profile")+1]
    else
        user=""
    console.log();
    console.log("test");
    $.ajax({
        url : '/ehealth/checkout_folder_ajax/', // the endpoint,commonly same url
        type : "POST", // http method
        data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                folder:folder,
                user:split_url[split_url.indexOf("profile")+1],
            }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log(data); // another sanity check
            //On success show the data posted to server as a message
            // location.reload();
            $("#modal_header").append("<h4 id='added_title'>" + folder + "</h4>");
            if(data['pages'])
            {
                var link_a,title_h4,summary_p,source_p,search_result;
                var pages = data["pages"]
                
                var delete_page = "<button type='button' class='btn btn-primary btn-danger mtb20 delete_page_button'>Delete</button>"
                
                
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
                    summary_p += pages[p]['summary'] + "</p>";
                    source_p += "Source: %s"%(pages[p]['source']) + "</p>";
                    link_a += title_h4 + summary_p + source_p + "</a>";
                    var scores = pages[p]['readability_score'] + " " +
                        pages[p]['subjectivity_score'] + " " + 
                        pages[p]['sentiment_score'] + " "
                    cont+= "<div class='col-md-10 mtb20 pull-left'>" + link_a+"</div>" + delete_page + scores + "</div>";
                    
                    $("#modal_body").append(cont);
                    
                    $(".delete_page_button").click(function(){
                        // console.log($(this).text());
                        // console.log($(this).parent().parent().children().text());
                        
                        // var folder = $("#choose_folder").text();
                        // var title = $(this).parent().parent().children(".pull-left").children("a").children("#title").text();
                        // var summary = $(this).parent().parent().children(".pull-left").children("a").children("#summary").text();
                        // var source = $(this).parent().parent().children(".pull-left").children("a").children("#source").text();
                        // var link = $(this).parent().parent().children(".pull-left").children("a").attr("href");
                        var link = $(this).parent().children(".pull-left").children("a").attr("href");
                        var row = $(this).parent();
                        // if($.trim(folder)=="Choose folder")
                        //     return
                        var folder = $("#added_title").text();
                        console.log(link);
                        $.ajax({
                                url : '/ehealth/delete_page_ajax/', // the endpoint,commonly same url
                                type : "POST", // http method
                                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                                        folder:folder,
                                        link:link,
                                        }, // data sent with the post request
    
                                // handle a successful response
                                success : function(data) {
                                    console.log(data);
                                    // console.log(row);
                                    // console.log(row.parent());
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