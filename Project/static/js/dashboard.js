$(document).ready(function(){
    $("input[name=search_bar]").val('');  //clear the input field in case it wasnt sanitised before that
    
    // Dropdown button for search category
    $(".category_option").click(function(){
        $("#category").text($(this).text());
    });
    
    
    $("#all_filter").click(function(){
        $(".showing").removeClass("showing");   //remove the class showing from the element which has it
        $(this).addClass("showing");            //and add it to this button
        
        $(".Bing, .Healthfinder, .MedlinePlus").show();     //show everything
    });
    
    $("#bing_filter").click(function(){
        $(".showing").removeClass("showing");   //remove the class
        $(this).addClass("showing");            //add it to this element
        
        $(".Bing").show();                      //show Bing
        $(".Healthfinder, .MedlinePlus").hide();//Hide everything which is not bing
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