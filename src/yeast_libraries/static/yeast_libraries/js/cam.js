$(document).ready(function()
{
	$img_cam = $('<img>',{
		id : "img_cam",
		src : "/static/yeast_libraries/img/noa_cam.jpg",
	    text: 'Back',
	    title: 'Back',
	    href: '#',
	    click: function(){ annoymous_snapshot();}
	});
	
	$('#div_cam').append($img_cam);

});

function snapshot()
{
	j = "kookoo=kookooer";
	console.log('getting snapshot');	
	$.get( "/yeast_libraries/simple_snapshot", j, function(data) 
		{
			console.log('data:');
			console.log(data);
			
			if(data=='cam_error')
			{
			  	alert('Camera failed to take a picture');
			  	retrun;
			}
			
			j = JSON.parse(data);
			
			img_path = j['image_path'];
			
			
			$img_cam.attr('src', img_path + "?time=" + new Date());	
		}
	);
}

function annoymous_snapshot()
{
	request = ''.concat('/yeast_libraries/annoymous_snapshot/?&random='+ Math.random());
	$img_cam.attr('src', request);
}
