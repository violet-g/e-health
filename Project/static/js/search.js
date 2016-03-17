// <a href="#" class="list-group-item  mtb20 table table-responsive">
//     <h4 class="list-group-item-heading mtb15">Title</h4>
//     <p class="list-group-item-text mtb10">Summary</p>
//     <p class="list-group-item-text mtb10">Source: Bing</p>
// </a>


$(document).ready(function(){

    //The purpose of this is so the All button is clicked by default
    //however it only works when this line is in a different js file
    //My guess is that is because (as far as I read) .trigger('click')
    //can be called only on jQuery objects with created click handlers
    //before trigger is called, and search.js is imported after dashboard.js
    $('#all_filter').trigger("click");  

    $("#search_button").click(function(){
        var query=$.trim($("input[name=search_bar]").val());
        $("input[name=search_bar]").val('');
        var category=$("#category").text();
        
        if(query=="")
            return;
        $("#search_results").empty();
        $.ajax({
            url : '/ehealth/search_ajax/', // the endpoint,commonly same url
            type : "POST", // http method
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    query:query,
                    category:category,
                    readability_score:5,
                    sentiment_score:8,
                    subjectivity_score:4,
                }, // data sent with the post request

            // handle a successful response
            success : function(data) {
                var link_a,title_h4,summary_p,source_p,search_result;
                
                console.log(data); // another sanity check
                //On success show the data posted to server as a message
                // location.reload();
                
                if(data["users"])  //format: list of dictionaries
                {
                    users=data["users"];
                    // for(var i in users)
                    //     console.log(i);
                    // console.log("maina"+data["users"]);
                    for(var i=0; i<users.length;i++)
                    {
                        link_a = "<a href='#' target='_blank' class='list-group-item  mtb20 table table-responsive'>"
                        username_h4= "<h4 class='list-group-item-heading mtb15'>"
                        names_p = "<p class='list-group-item-text mtb10'>"
                        email_p = "<p class='list-group-item-text mtb10'>"
                        
                        //for localhost
                        link_a = link_a.replace("#", "localhost:8000/ehealth/" + users[i]["username"]);
                        
                        //for Zdravko
                        // link_a = link_a.replace("#", "https://e-health-mega-qkiq-pich.c9users.io/ehealth/" + users[i]["username"]);
                        
                        username_h4 += users[i]['username'] + "</h4>";
                        names_p += users[i]['first_name']+ " " + users[i]['last_name'] + "</p>";
                        email_p += "Email:" + users[i]['email'] + "</p>"
                        link_a += username_h4 + names_p + email_p + "</a>";
                        console.log(link_a);
                        $("#search_results").append(link_a);
                    }
                }
                var bing=0;
                var medlineplus=0;
                var healthfinder=0;
                var sources={}
                //filter the cases of empty answers
                if (data['bing_result'])
                {
                    bing=data['bing_result'];
                    sources["Bing"]=bing;
                }
                if (data['medlineplus_result'])
                {
                    medlineplus=data['medlineplus_result'];
                    sources["MedlinePlus"]=medlineplus;
                }
                if (data['healthfinder_result'])
                {
                    healthfinder=data['healthfinder_result'];
                    sources["Healthfinder"]=healthfinder;
                }   
                var len = 0;
                for(var i in sources)
                    if(len<sources[i].length)
                        len=sources[i].length;
                // sources={"MedlinePlus":medlineplus,"Healthfinder":healthfinder,"Bing":bing};
                for(var i=0;i<len; i++)
                {
                    for(var s in sources)
                    {
                        if(sources[s].length<i)
                            continue;
                            
                        //s is the value of the key in the Dictionary AND the class added in the htm
                        link_a = "<a href='#' target='_blank' class='list-group-item  mtb20 table table-responsive "+s+ "'>"
                        title_h4= "<h4 class='list-group-item-heading mtb15'>"
                        summary_p = "<p class='list-group-item-text mtb10'>"
                        source_p = "<p class='list-group-item-text mtb10'>"

                        link_a = link_a.replace("#",sources[s][i]['link']);
                        title_h4 += sources[s][i]['title'] + "</h4>";
                        summary_p += sources[s][i]['summary'] + "</p>";
                        source_p += "Source: Bing" + "</p>"
                        link_a += title_h4 + summary_p + source_p + "</a>";
                        $("#search_results").append(link_a);
                        
                    }
                };
                $(".showing").trigger('click');
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
         });
    });
    //trigger click of the button on enter
    $("#search_bar").keypress(function(event){
        if (event.which == 13) {
            $("#search_button").trigger('click');
        }
    })

})