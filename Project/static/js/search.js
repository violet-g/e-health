$(document).ready(function(){

    //The purpose of this is so the All button is clicked by default
    //however it only works when this line is in a different js file
    //My guess is that is because (as far as I read) .trigger('click')
    //can be called only on jQuery objects with created click handlers
    //before trigger is called, and search.js is imported after dashboard.js
    $('#all_filter').trigger("click");
    
    $("#loading").hide(); //hide icon
    $("#loading_results").hide();   //hide the box with "Results for: "
    
    
    $("#search_button").click(function(){
        var query=$.trim($("input[name=search_bar]").val());
        $("input[name=search_bar]").val('');
        
        var category=$("#category").text();
        
        //if query is empty do nothing
        if(query=="")
            return;
        
        //remove the results and other unnecesary elements from prev searches
        $("#search_results").empty();
        
        $("#loading_results").hide();
        $("#loading_results").empty();
        
        $("#loading").show();   //show it until we get the data
        $("#loading_results").append("<h4 class='text-center searched_query'> <em> Results for: "+query + "</em> </h4>");
        
        $.ajax({
            url : '/ehealth/search_ajax/', // the endpoint,commonly same url
            type : "POST", // http method
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    query:query,
                    category:category,
                    readability_score:$("#r_score").val(),
                    sentiment_score:$("#s_score").val(),
                    subjectivity_score:$("#ss_score").val(),
                    number_of_results:$("results_from_search").val(),
                }, // data sent with the post request

            // handle a successful response
            success : function(data) {
                var link_a,title_h4,summary_p,source_p,search_result,username_h4,names_p,email_p;
    
                $("#loading").hide();   //data is here, clear the loading ico
                $("#loading_results").show();

                if(data["users"])  //format: list of dictionaries
                {
                    var users=data["users"];
                    
                    for(var i=0; i<users.length;i++)
                    {
                        link_a = "<a href='#' target='_blank' class='list-group-item mtb20 table table-responsive'>"
                        username_h4= "<h4 class='list-group-item-heading mtb15'>"
                        names_p = "<p class='list-group-item-text mtb10'>"
                        email_p = "<p class='list-group-item-text mtb10'>"
                        
                        link_a = link_a.replace("#", "/ehealth/profile/" + users[i]["username"] + '/');
                        
                        username_h4 += users[i]['username'] + "</h4>";
                        names_p += users[i]['first_name']+ " " + users[i]['last_name'] + "</p>";
                        email_p += "Email:" + users[i]['email'] + "</p>"
                        link_a += username_h4 + names_p + email_p + "</a>";

                        $("#search_results").append(link_a);
                    }
                }
                var bing=0;
                var medlineplus=0;
                var healthfinder=0;
                var sources={}

                //filter the cases of empty answers
                if (data['bing_result'] && data['bing_result'].length)
                {
                    bing=data['bing_result'];
                    sources["Bing"]=bing;
                }
                if (data['medlineplus_result'] && data['medlineplus_result'].length)
                {
                    medlineplus=data['medlineplus_result'];
                    sources["MedlinePlus"]=medlineplus;
                }
                if (data['healthfinder_result'] && data['healthfinder_result'].length)
                {
                    healthfinder=data['healthfinder_result'];
                    sources["Healthfinder"]=healthfinder;
                }   
                var len = 0;

                //var len is the length of the longest source
                //so that we can present max elements later on
                for(var i in sources)
                    if(len<sources[i].length)
                        len=sources[i].length;
                
                //add to folder button with dropdown
                var add_to_folder = "<div class='col-md-3 mtb20 pull-right'>" +
                                      "<button type='button' class='btn btn-block btn-success add_to_folder_button'>" +
                                        "Add to folder" +
                                      "</button>" +
                                      "<button type='button' class='btn btn-block btn-default dropdown-toggle folder_choice_button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
                                        "Choose folder" +
                                      "</button>" +
                                      "<ul class='dropdown-menu folder_options btn-block '>"
                
                
                var items;
                $(".folder").each(function(){
                    add_to_folder+= "<li class='folder_choice'><a href='#!'>" + $(this).text() + "</a></li>";
                });
                add_to_folder+="</ul>" + "</div>";
                
                //go through len elements in all sources
                for(var i=0;i<len; i++)
                {
                    for(var s in sources)
                    {
                        //if that source doesnt have that many items
                        //go on to the next one
                        if(sources[s].length<=i)
                            continue;
                        
                        //wrap the link in a div and the buttons in another div
                        
                        var cont = "<div class='row "+ s + "'>"       
                        
                        link_a = "<a id='link' href='#' target='_blank' class='list-group-item table table-responsive'>"
                        title_h4= "<h4 id='title' class='list-group-item-heading mtb15'>"
                        summary_p = "<p id='summary' class='list-group-item-text mtb10'>"
                        source_p = "<p id='source' class='list-group-item-text mtb10'>"
                        
                        link_a = link_a.replace("#",sources[s][i]['link']);
                        title_h4 += sources[s][i]['title'] + "</h4>";
                        summary_p += sources[s][i]['summary'].slice(0,300)+"..." + "</p>";
                        source_p += "Source: "+ s + "</p>"
                        link_a += title_h4 + summary_p + source_p + "</a>";
                        
                        cont+= "<div class='col-md-9 mtb20 pull-left'>" + link_a+"</div>" + add_to_folder + "</div>"
                        
                        $("#search_results").append(cont);
                        
                        
                    }
                };
                $(".showing").trigger('click');
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $("#loading").hide();   //Something broke. User shouldn't wait
                // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
         });
    });
    //trigger click of the button on enter
    $("#search_bar").keypress(function(event){
        if (event.which == 13) {
            $("#search_button").trigger('click');
        }
    });
    
    //change the choices in the dropdown button under add to folder
    $("body").on("click",".folder_choice", function(){
        $(this).parent().parent().children(".folder_choice_button").text($(this).text());
    });
    
    
    $("body").on('click','.add_to_folder_button', function(){
        var folder = $(this).parent().children(".folder_choice_button").text();
        
        // if a folder is not chosen do nothing
        if($.trim(folder)=="Choose folder")
            return;
        
        var title = $(this).parent().parent().children(".pull-left").children("a").children("#title").text();
        var summary = $(this).parent().parent().children(".pull-left").children("a").children("#summary").text();
        
        var source = $(this).parent().parent().children(".pull-left").children("a").children("#source").text();
        source=$.trim(source.split("Source:")[1]); //remove the "Source:" part of the string
        
        var link = $(this).parent().parent().children(".pull-left").children("a").attr("href");
            
        $.ajax({
                url : '/ehealth/add_page_ajax/', // the endpoint,commonly same url
                type : "POST", // http method
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                        folder:folder,
                        link:link,
                        title:title,
                        summary:summary,
                        source:source,
                        }, // data sent with the post request

                // handle a successful response
                success : function(data) {
                    // console.log(data);
                    // the backend handles the request
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
        })
        
    });


})
