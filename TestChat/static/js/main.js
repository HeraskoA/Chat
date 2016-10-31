function submit() {
$('#ch').click(function(event){
var text = $(".form-control").val();
$.ajax({
'type': 'POST',
'dataType': 'json',
'data': {	
	'mess': text,	
	'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	},

'error': function(xhr, status, error){alert("jшибка");},
'success': function(data, status, xhr){
if (data != []) {
var dialogWindow = $('.message')
$.each(data, function() {
dialogWindow.append('<p><address>' + this.sender + '</address><span>' + this.text + '</span>');
});
scrol();
}}
});
$('.form-control').val('');
return false;
});
}


function scrol() {
var div = $("#chat-messages");
div.scrollTop(div.prop('scrollHeight'));}

function update() {
$.ajax({
'dataType': 'json',
'type': 'get',
'error': function(xhr, status, error){alert("oшибка");},
'success': function(data, status, xhr) {
if (data != []) {
var dialogWindow = $('.message')
$.each(data, function() {
dialogWindow.append('<p><address>' + this.sender + '</address><span>' + this.text + '</span>');
scrol();
});
}}
});
}


$(document).ready(function(){
scrol();
submit();
if (window.location.href.indexOf('dialog') + 1) { 
update(); 
setInterval('update()', 1000);
};

});
