$(function(){
	$('#addmember').click(function(){

		$.ajax({
			url: '/addMember',
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
