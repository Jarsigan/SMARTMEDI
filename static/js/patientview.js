$(function(){
	$('#viewpatient').click(function(){
alert("hhhhh");
		$.ajax({
			url: '/viewHome',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});