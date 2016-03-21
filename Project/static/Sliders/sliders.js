$(function(){

	$("#slider1").slider({
		range:"min",
		value: 0,
		min: 0,
		max: 100,
		slide: function(event,ui){
			$("#r_score").val(ui.value);
		}
	});	
	$("#r_score").val($("#slider1").slider("value"));

	$("#slider2").slider({
		range:"min",
		value: 0,
		min: 0,
		max: 100,
		slide: function(event,ui){
			$("#s_score").val(ui.value);
		}
	});	
	$("#s_score").val($("#slider2").slider("value"));

	$("#slider3").slider({
		range:"min",
		value: 0,
		min: 0,
		max: 100,
		slide: function(event,ui){
			$("#ss_score").val(ui.value);
		}
	});	
	$("#ss_score").val($("#slider3").slider("value"));
});
