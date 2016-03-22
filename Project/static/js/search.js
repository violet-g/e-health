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
                    readability_score:$("#r_score").val(),
                    sentiment_score:$("#s_score").val(),
                    subjectivity_score:$("#ss_score").val(),
                    number_of_results:$("results_from_search").val(),
                }, // data sent with the post request

            // handle a successful response
            success : function(data) {
                var link_a,title_h4,summary_p,source_p,search_result,username_h4,names_p,email_p;
                              
                
                console.log(data); // another sanity check
                //On success show the data posted to server as a message
                // location.reload();
                if(data["users"])  //format: list of dictionaries
                {
                    var users=data["users"];
                    // for(var i in users)
                    //     console.log(i);
                    // console.log("maina"+data["users"]);
                    
                    for(var i=0; i<users.length;i++)
                    {
                        link_a = "<a href='#' target='_blank' class='list-group-item mtb20 table table-responsive'>"
                        username_h4= "<h4 class='list-group-item-heading mtb15'>"
                        names_p = "<p class='list-group-item-text mtb10'>"
                        email_p = "<p class='list-group-item-text mtb10'>"
                        
                        //for localhost
                        link_a = link_a.replace("#", "/ehealth/profile/" + users[i]["username"] + '/');
                        
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
                for(var i in sources)
                    if(len<sources[i].length)
                        len=sources[i].length;
                // sources={"MedlinePlus":medlineplus,"Healthfinder":healthfinder,"Bing":bing};
                // var add_to_folder = "<div class='btn-group col-md-2 mtb20 pull-right'>" +
                //                       "<button type='button' class='btn btn-success dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
                //                         "Action" +
                //                       "</button>" +
                //                       "<ul class='dropdown-menu'>" +
                //                         "<li><a href='#'>Action</a></li>" +
                //                         "<li><a href='#'>Another action</a></li>" +
                //                         "<li><a href='#'>Something else here</a></li>" +
                //                         "<li role='separator' class='divider'></li>" +
                //                         "<li><a href='#'>Separated link</a></li>" +
                //                       "</ul>" +
                //                     "</div>";
                
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
                
                
                for(var i=0;i<len; i++)
                {
                    for(var s in sources)
                    {
                        if(sources[s].length<=i)
                            continue;
                     
                        var cont = "<div class='row "+ s + "'>"       
                        
                        link_a = "<a id='link' href='#' target='_blank' class='list-group-item table table-responsive'>"
                        title_h4= "<h4 id='title' class='list-group-item-heading mtb15'>"
                        summary_p = "<p id='summary' class='list-group-item-text mtb10'>"
                        source_p = "<p id='source' class='list-group-item-text mtb10'>"
                        
                        link_a = link_a.replace("#",sources[s][i]['link']);
                        title_h4 += sources[s][i]['title'] + "</h4>";
                        summary_p += sources[s][i]['summary'] + "</p>";
                        source_p += "Source: "+ s + "</p>"
                        link_a += title_h4 + summary_p + source_p + "</a>";
                        var scores = sources[s][i]['readability_score'] + " " +
                        sources[s][i]['subjectivity_score'] + " " + 
                        sources[s][i]['sentiment_score'] + " "
                        
                        cont+= "<div class='col-md-9 mtb20 pull-left'>" + link_a+"</div>" + add_to_folder + scores + "</div>"
                        // $("#search_results").append(link_a);
                        // $("#search_results").append(add_to_folder);
                        $("#search_results").append(cont);
                        // $("#search_results").append(add_to_folder);
                        
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
    });
    
    // $(".folder_choice").click(function(){
    $("body").on("click",".folder_choice", function(){
        // $(this).parent().children(".folder_choice_button").text();
        // $(".folder_choice_button").text($(this).text());
        // console.log($(this).parent().parent().children(".folder_choice_button").text());
        $(this).parent().parent().children(".folder_choice_button").text($(this).text());
    });
    // $(".add_to_folder_button").click(function(){
    $("body").on('click','.add_to_folder_button', function(){
        // console.log($(this).text());
        // console.log($(this).parent().parent().children().text());
        var folder = $(this).parent().children(".folder_choice_button").text();
        // var folder = $(".folder_choice_button").text();
        var title = $(this).parent().parent().children(".pull-left").children("a").children("#title").text();
        var summary = $(this).parent().parent().children(".pull-left").children("a").children("#summary").text();
        var source = $(this).parent().parent().children(".pull-left").children("a").children("#source").text();
        var link = $(this).parent().parent().children(".pull-left").children("a").attr("href");
        if($.trim(folder)=="Choose folder")
            return
        // console.log()
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
                    console.log(data);
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
        })
        
        
        // console.log($(this).parent().parent().parent())
        // var txt=$(this).text().substr(0,15);
        // if(txt.length < $(this).text().length)
        //     txt+="..."
    });


})