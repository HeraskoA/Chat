function submit() {
	$('#ch').click(function(event){
		var text = $(".form-control").val();
		var pattern = /^[\s]+$/;
		if (!pattern.test(text)) {
			$.ajax({
				'type': 'POST',
				'dataType': 'json',
				'data': {	
					'mess': text,	
					'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
						}
			});
		};
		$('.form-control').val('');
		return false;
		});
}


function scroll() {
	var div = $("#chat-messages");
	div.scrollTop(div.prop('scrollHeight'));
}

function update() {
	$.ajax({
		'dataType': 'json',
		'type': 'get',
		'data': {	
			'count': count
		},
		'success': function(data, status, xhr) {
			if (data != []) {
				var dialogWindow = $('.message')
				$.each(data, function() {
					dialogWindow.append('<p><address>' + this.sender + '</address><span>' + this.text + '</span><div id="date">' + this.time + '</div>');
					count = count + 1;
					scroll();
				});
			}
		}
	});
}


$(document).ready(function(){
    scroll();
    submit();
    update(); 
    setInterval('update()', 1000);
});
