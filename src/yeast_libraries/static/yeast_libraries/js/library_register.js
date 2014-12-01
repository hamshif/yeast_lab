


$(document).ready(function(){	
	
	$('#input_file').change(function(){
   	
	    filename = $("#input_file").val();
	    ext = filename.substr(filename.lastIndexOf('.') + 1);
	    
	    //console.log(ext);
	    
	    if(ext == 'xls')
	    {
	    	
	    }
	    else
	    {
	    	alert('this field only accepts Excel files of the type .xls');
	    }
	});
});



function createLibraryRegisterForm(parent_element, update)
{	
	parent_element.append('<h1>Upload Library Excel</h1>');
	
	$f_lib = $('<form></form>', {
		id : "f_lib",
		action :"/yeast_libraries/library_copier/",
		method: "post",
		enctype: "multipart/form-data",
		name: "f_lib"
	});

	
	parent_element.append($f_lib);
	
		$input_file = $('<input>', {
			id: "input_file",
			type:"file",
			name: "input_file"
			
		});
		
		$f_lib.append($input_file);
		
		$f_lib.append('<h2>Nickname<h2>');
		
		$t_personal_name = $('<input>', {
			
			id: "t_personal_name",
			type:"text",
			name: "t_personal_name",
			value: COMMON_USER
		});
		
		$f_lib.append($t_personal_name);
		
		$f_lib.append('<br></br>');
		
		
		$input_submit = $('<input>', {
			id: "input_submit",
			type:"button",
			click: function(){ postForm();},
			value: "submit library or plate"
		});
		
		$f_lib.append($input_submit);
		
		
	$div_msg = $('<div>', {
		id: 'div_msg'
	});
	
	$f_lib.append($div_msg);
	
	//$div_msg.append('<h1>Progress Message<h1>');
	
	$p_lib_reg_progress_msg = $('<p>',{
		
		id: "p_lib_reg_progress_msg",
		class: "progress_message",
		text: "Progress Message"
	});
	
	$div_msg.append($p_lib_reg_progress_msg);


    $img_lib_format_help = $('<img>', {

        id: "img_lib_format_help",
        src: "/static/lab/img/help.png",
        click: function(){alert('To see an example of the correct format click the green "Library CSV" button below\n\nSave the file as .xls\n\nFile name will be the library name and should have no spaces or funny characters\n\nFirst excel row will hold column names [plate, row, column, strain] in this order\n\nSubsequent Excel rows will hold:\n\nExcel column 1 will hold plate number values 1-n in that order\n\nSecond Excel column will hold row index in capital letters in alphabetical order\n\n3rd row will hold column index 1-n\n\nDo not enter empty matrix loci\n\nDo not insert empty columns or rows');}

    });

    parent_element.append($img_lib_format_help);
	
	this.postForm = function ()
	{
		//console.log('postForm()');
		
		// $div_msg.empty();
		// $div_msg.append('<h1>uploading wait for message or browse<h1>');
		
		$p_lib_reg_progress_msg.empty();
		$p_lib_reg_progress_msg.append('<p>' + 'Uploading' + '</p>');
		
		try
		{
			filename = $("#input_file").val();
			ext = filename.substr(filename.lastIndexOf('.') + 1);
		}
		catch(err) 
		{
		    alert('this form only accepts Excel files of the type .xls');
	    	return;
		}
	    
	    //console.log(ext);
	    
	    if(ext == 'xls')
	    {
	    	
	    }
	    else
	    {
	    	alert('this form only accepts Excel files of the type .xls');
	    	return;
	    }	
		
		var files = $input_file[0].files;
		var formData = new FormData();
		
		for (var i = 0; i < files.length; i++) 
		{
		  var file = files[i];
           console.log('file.name: ', file.name);
		  console.log('file.type: ', file.type);
		  // Check the file type.
		  // if (!file.type.match('image.*')) {
		    // continue;
		  // }
		
		  // Add the file to the request.
		  formData.append('input_file', file, file.name);
		}
		
		
	// 		
		// is_liquid = $cb_is_liquid.is(":checked");
		personal_name = $t_personal_name.val();
	// 	
		//console.log('is_liquid: ', is_liquid);
		console.log('personal_name: ', personal_name);
	// 	
		// formData.append('is_liquid', is_liquid);
		formData.append('personal_name', personal_name);

        //console.log('formData: ', formData);
		
		var xhr = new XMLHttpRequest();
		xhr.onload = libRegisterCallback;
		xhr.open('POST', '/yeast_libraries/library_copier/', true);

        console.log('csrftoken: ', csrftoken);

		xhr.setRequestHeader("X-CSRFToken", csrftoken);
		console.log(xhr);
		
		xhr.send(formData);
	};
	
	
	this.libRegisterCallback = function () 
	{
		//console.log('this.responseText: ', this.responseText);
		// $div_msg.empty();
		// $div_msg.append('<h1>' + this.responseText + '<h1>');
		
		$p_lib_reg_progress_msg.empty();
		$p_lib_reg_progress_msg.append('<p>' + this.responseText + '</p>');
		
		if(update != undefined)
		{
			update();
		}
	};
}









