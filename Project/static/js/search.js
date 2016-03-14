$(document).ready(function(){

    $("#search_button").click(function(){
        var query=$.trim($("input[name=search_bar]").val());
        $("input[name=search_bar]").val('');
        var category=$("#category").text();
        if(query=="")
            return;
        $.ajax({
            url : '/ehealth/search_ajax/', // the endpoint,commonly same url
            type : "POST", // http method
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    query:query,
                    category:category
                }, // data sent with the post request

            // handle a successful response
            success : function(data) {
                console.log(data); // another sanity check
                //On success show the data posted to server as a message
                // location.reload();
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
         });
    });


})