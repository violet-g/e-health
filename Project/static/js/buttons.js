$(document).ready(function(){
    $(".active_on_hover").hover(function(){
       $(this).toggleClass("active"); 
    });
    
    $(".nav a").on("click", function(){
       $(".nav").find(".active").removeClass("active");
       $(this).parent().addClass("active");
    });
})