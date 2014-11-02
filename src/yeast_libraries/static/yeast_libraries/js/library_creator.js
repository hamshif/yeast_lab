var csrftoken;

$(document).ready(function()
{
	//console.log('library_creator.js');
	csrftoken = getCookie('csrftoken');
	//console.log('csrftoken: ', csrftoken);
	
	createLibraryRegisterForm($('#div_form'));
});