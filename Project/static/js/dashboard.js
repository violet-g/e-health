$(document).ready(function(){
    $(".btn").click(function(){
        $.get('/ehealth/test_ajax',{},function(data){
            // alert(data);
        });
    });
});