

$(document).ready(function()
{
	csrftoken = getCookie('csrftoken');
	
	$div_stack_reg = $('#div_stack_reg');
	
	copyRegister = new CopyRegister('stack_register', copyRegisterCallback);
	copyRegister.createRegisterStackGUI($div_stack_reg);
 	copyRegister.getAndDisplayDataFromServer(COMMON_USER);
});


function copyRegisterCallback(responseText) 
{
	console.log('methushelach');
	console.log('this.responseText: ', responseText);
	
	
	console.log('fleishier');
	// $div_msg.empty();
	// $div_msg.append('<h1>' + this.responseText + '<h1>');
}