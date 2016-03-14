$(document).ready(function(){
    // $(".btn").click(function(){
    //     $.get('/ehealth/test_ajax',{},function(data){
    //         // alert(data);
    //     });
    // });
    $(".category_option").click(function(){
        $("#category").text($(this).text());
    });
});