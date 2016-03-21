$(document).ready(function(){
    $(".slider").slider();
    
    $('#ex1').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	    }
    });
})