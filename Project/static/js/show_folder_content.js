
$(".folder").dblclick(function(){
    var folder = $(this).text();
    // console.log(folder);
    
    console.log("test");
    $.ajax({
        url : '/ehealth/checkout_folder_ajax/', // the endpoint,commonly same url
        type : "POST", // http method
        data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                folder:folder
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
                for(var p in pages)
                {
                    console.log(pages[p]);
                    console.log(pages[p]['url']);
                    console.log(pages[p]['summary']);
                    console.log(pages[p]['source']);
                    // $("#modal_body").append("<p>" + "</p>");
                    
                    link_a = "<a href='#' target='_blank' class='list-group-item  mtb20 table table-responsive '>"
                    title_h4= "<h4 class='list-group-item-heading mtb15'>"
                    summary_p = "<p class='list-group-item-text mtb10'>"
                    source_p = "<p class='list-group-item-text mtb10'>"
                    
                    link_a = link_a.replace("#",pages[p]['url']);
                    title_h4 += pages[p]['title'] + "</h4>";
                    summary_p += pages[p]['summary'] + "</p>";
                    source_p += "Source: %s"%(pages[p]['source']) + "</p>"
                    link_a += title_h4 + summary_p + source_p + "</a>";
                    $("#modal_body").append(link_a);
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