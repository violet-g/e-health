$(document).ready(function(){
    $("#delete_folder").click(function(){
        console.log($("#folder_list").children(".active").children("a:first").text());
    })
})