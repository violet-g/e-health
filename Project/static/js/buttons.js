$(document).ready(function(){
    //click handler for items with active_on_click
    $(".active_on_click").click(function(){
       $(".active").removeClass("active");
       $(this).toggleClass("active");
    });
    
    
    //menu on the left - clickable and slectable
    $("body").on("click",".nav a", function(){
       $(".nav").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
    
    //buttons for folder publicity in profile - switch between Public/Hidden
    $("body").on("click", ".privacy_button", function(){
        $(this).toggleClass("btn-danger btn-success")
        var text = $(this).text();
        if($.trim(text)=="Public")
            $(this).text("Hidden");
        else
            $(this).text("Public");
        $("#save_folder_changes").removeClass("disabled");
    });
    
})