//on hide remove the added element to the modal, since we dont need it anymore
$('#myModal').on('hidden.bs.modal',function(){
    $("#modal_header").empty();
    $("#modal_body").empty();
    $("#delete").remove();
    $("#create").remove();
});