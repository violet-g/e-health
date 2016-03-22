$(document).ready(function(){
    $.ajax({
        url : '/ehealth/privacy_details_ajax/', // the endpoint,commonly same url
        type : "GET", // http method
        data : {
            }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log(data);
            console.log($(".privacy_details_button"));
            // $(".privacy_details_button.active").removeClass("active");
            if(data['public']==true)
            {
                console.log("true");
                $(".privacy_details_button.btn-danger").addClass('active');
            }
            else if(data['public']==false)
            {
                console.log("false");
                $(".privacy_details_button.btn-success").addClass('active');
            }
        },
        
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    
    $("#save_folder_changes").on('click',function(){
        if($(this).hasClass('disabled'))
            return;
        var data=[];
        $(".folder").each(function(){
            console.log($(this).text())
            console.log($(this).next(".privacy_button").text())
            data.push({folder:$.trim($(this).text()),
                    privacy:$.trim($(this).next(".privacy_button").text()),
                    });
        })
        $.ajax({
                url : '/ehealth/save_folder_privacy_ajax/',
                type : "POST",
                data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    "folders":JSON.stringify(data),
                    },
                success : function(data){
                    console.log(data);
                    $("#save_folder_changes").addClass('disabled');
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }

            });
    });
    
    $(".privacy_details_button").click(function(){
        console.log($(this).text());
        $.ajax({
                url : '/ehealth/privacy_details_ajax/', // the endpoint,commonly same url
                type : "POST", // http method
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 
                        publicity:$.trim($(this).text()),
                    }, // data sent with the post request
        
                // handle a successful response
                success : function(data) {
                    
                },
                
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
    })
})