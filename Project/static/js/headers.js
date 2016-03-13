$(document).ready(function(){
    $(".active_on_hover").hover(function(){
       $(this).toggleClass("active"); 
    });
    $("#header").css({borderRadius: "10px"});
    // $("#middle").css({borderRight: "1px", borderLeft: "1px"});
})