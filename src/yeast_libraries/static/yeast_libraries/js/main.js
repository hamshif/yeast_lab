
var ALL_NICKNAMES = 'ALL_NICKNAMES';
var COMMON_USER = 'everyone';

var MAIN_CONTEXT = 'main';
var COMPARED_CONTEXT = 'compared';
var LIQUID_CONTEXT = 'liquid_plate_analysis';


function putImageIn(img_path, recepticle)
{	
	if(img_path.indexOf('/static') === 0)
	{
		recepticle.attr('src', img_path);
	}
	else
	{
		var request = ''.concat('/yeast_libraries/get_image/?image_full_path=', img_path, "&random=" + Math.random());
		recepticle.attr('src', request);
	}
	
	//console.log('put: ', img_path, ' in: ', recepticle.attr('id'));
}



function getSelectedText(id)
{
	e = document.getElementById(id);
	v = e.selectedIndex;
	//console.log("selected index:  " + v);
	
	if(v != -1)
	{
		g = e.options[v].text;
		//console.log("value:  " + g);
	}
	else
	{		
		return -1;	
	}
	
	return g;
}


function retrieveSelectedText(selector)
{
	v = selector.selectedIndex;
	console.log("selected index:  " + v);
	
	if(v != -1)
	{
		g = selector.options[v].text;
		//console.log("value:  " + g);
	}
	else
	{		
		return -1;	
	}
	
	return g;
}



function getSelectedValue(id)
{
	e = document.getElementById(id);
	v = e.selectedIndex;
	//console.log("selected index:  " + v);
	
	if(v != -1)
	{
		g = e.options[v].value;
		//console.log("value:  " + g);
	}
	else
	{		
		return -1;	
	}
	
	return g;
}


function endsWith(str, suffix) 
{
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}