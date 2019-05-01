$(function(){
	$('#addPatient').click(function(){

		$.ajax({
			url: '/addPatient',
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
