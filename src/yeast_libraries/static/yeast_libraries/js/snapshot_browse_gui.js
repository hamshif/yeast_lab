
function createSnapshotGUI(plateMap, parent_element, update)
{
	$current_batch_browser = $('<div id="current_batch_browser"></div>');
			
	$current_batch_counter = $('<h2 id="batch_label", class="batch_gui">No Batches A</h2>');

	$current_batch_browser.append($current_batch_counter);

	$img_current_batch_back = $('<img>',{
		id : "current_batch_back",
		class : "batch_gui",
		src : "/static/yeast_libraries/img/back.png",
	    text: 'Back',
	    title: 'Back',
	    href: '#',
	    click: function(){update(plateMap.dataMap, false);}
	});
	
	$current_batch_browser.append($img_current_batch_back);
	
	
	$img_current_batch_next = $('<img>',{
		id : "current_batch_next",
		class : "batch_gui",
		src : "/static/yeast_libraries/img/next.png",
	    text: 'Next',
	    title: 'Next',
	    href: '#',
	    click: function(){update(plateMap.dataMap, true);}
	});

	$current_batch_browser.append($img_current_batch_next);
	
	
	parent_element.append($current_batch_browser);
}