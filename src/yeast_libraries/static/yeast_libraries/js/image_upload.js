


function createImageUpload(parent_element, plateMap)
{
    var iu = this;

//    console.log(iu);

    $input_image = $('<input>', {

        id: "input_image",
        type:"file",
        name: "input_image"

    });

    parent_element.append($input_image);


	$b_new_batch1 = $('<input>', {
		id : "b_new_batch1",
		class : "upload_image",
		type : "button",
		value: "Same Batch",
		click: function(){

			if($(this).val() == "Same Batch")
			{
				$(this).prop('value', "New Batch");
			}
			else
			{
				$(this).prop('value', "Same Batch");
			}
		}

	});

	parent_element.append($b_new_batch1);


    parent_element.append('<br>');

	$img_upload1 = $('<img>',{
		id : "img_upload1",
		src : "/static/lab/img/upload.png",
	    text: 'This is blah',
	    title: 'Blah',
	    href: '#',
	    click: function(){ console.log('dude?!!'); iu.postForm1();}
	});

	parent_element.append($img_upload1);


    var p_image_upload_progress_msg = $('<p>',{

		id: "p_image_upload_progress_msg",
		class: "progress_message",
		text: "Progress Message"
	});

	parent_element.append(p_image_upload_progress_msg);



    this.postForm1 = function ()
	{
//		console.log('postForm()');

		p_image_upload_progress_msg.empty();
		p_image_upload_progress_msg.append('<p>' + 'Uploading' + '</p>');

        var filename;
        var ext;

		try
		{
			filename = $("#input_image").val();
			ext = filename.substr(filename.lastIndexOf('.') + 1);
		}
		catch(err)
		{
		    alert('this form only accepts Excel files of the type .jpg');
	    	return;
		}

	    console.log(ext);

	    if(ext == 'jpg' || ext == 'jpeg')
	    {

	    }
	    else
	    {
	    	alert('this form only accepts Excel files of the type .jpeg or .jpg');
	    	return;
	    }

		var files = $input_image[0].files;

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
             formData.append('input_image', file, file.name);
		}


        var query = snapshotQuery(plateMap, true);

        //console.log(JSON.stringify(query));

        formData.append('json_snapshot_info', JSON.stringify(query));

        console.log('formData: ', formData);



		var xhr = new XMLHttpRequest();
		xhr.onload = this.imageUploadCallback;
		xhr.open('POST', '/yeast_libraries/snapshot/', true);

        console.log('csrftoken: ', csrftoken);

		xhr.setRequestHeader("X-CSRFToken", csrftoken);
		console.log(xhr);

		xhr.send(formData);
	};


	this.imageUploadCallback = function ()
	{

		p_image_upload_progress_msg.empty();
		p_image_upload_progress_msg.append('<p>' + this.responseText + '</p>');

		if(update != undefined)
		{
			update();
		}
	};
}