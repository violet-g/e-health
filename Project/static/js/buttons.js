$(document).ready(function(){
    $(".active_on_click").click(function(){
       $(".active").removeClass("active");
       $(this).toggleClass("active");
    });
    
    $(".nav a").on("click", function(){
       $(".nav").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
})