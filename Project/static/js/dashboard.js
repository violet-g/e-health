$(document).ready(function(){
    $("input[name=search_bar]").val('');  //clear the input field in case it wasnt sanitised before that
    
    // $(".btn").click(function(){
    //     $.get('/ehealth/test_ajax',{},function(data){
    //         // alert(data);
    //     });
    // });
    $(".category_option").click(function(){
        $("#category").text($(this).text());
    });
    
    
    $("#all_filter").click(function(){
        $(".showing").removeClass("showing");
        $(this).addClass("showing");
        
        $(".Bing, .Healthfinder, .MedlinePlus").show();
    });
    $("#bing_filter").click(function(){
        $(".showing").removeClass("showing");
        $(this).addClass("showing");
        
        $(".Bing").show();
        $(".Healthfinder, .MedlinePlus").hide();
    });
    $("#healthfinder_filter").click(function(){
        $(".showing").removeClass("showing");
        $(this).addClass("showing");
        
        $(".Healthfinder").show();
        $(".Bing, .MedlinePlus").hide();
    });
    $("#medlineplus_filter").click(function(){
        $(".showing").removeClass("showing");
        $(this).addClass("showing");
        
        $(".MedlinePlus").show();
        $(".Healthfinder, .Bing").hide();
    });
    
});