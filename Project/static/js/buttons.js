$(document).ready(function(){
    $(".active_on_click").click(function(){
       $(".active").removeClass("active");
       $(this).toggleClass("active");
    });
    
    $("body").on("click",".nav a", function(){
       $(".nav").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
    
    $("body").on("click", ".privacy_button", function(){
        $(this).toggleClass("btn-danger btn-success")
        var text = $(this).text();
        if($.trim(text)=="Public")
            $(this).text("Hidden");
        else
            $(this).text("Public");
        $("#save_folder_changes").removeClass("disabled");
    });
    
    // $(".public_details_button").click(function(){
    //     // $(".public_details_button, .hidden_details_button").removeClass("active");
    //     $(".public_details_button").button('toggle');
    //     $(".hidden_details_button").button('toggle');
    //     // $(this).button('toggle');
    //     // $(this).addClass('active');
    // })
})