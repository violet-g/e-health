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
	
	$("#slider4").slider({
		range:"min",
		value: 0,
		min: 0,
		max: 100,
		slide: function(event,ui){
			$("#results_from_search").val(ui.value);
		}
	});	
	$("#results_from_search").val($("#slider4").slider("value"));
	
	// console.log($(".slider").slider('value'));
	
	// $(".slider").each(function(){
	// 	var t = $(this).prev("h4").text();
	// 	$(this).prev("h4").text(t+ " " + $(this))
	// });
});
