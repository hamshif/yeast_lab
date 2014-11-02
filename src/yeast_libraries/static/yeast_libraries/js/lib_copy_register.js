
function populateLibCopyGUI(plateMap, libraryFilter, parent_element, lib_form_element, user_selector)
{
	//console.log('populateLibCopyGUI', plateMap);
	populateLibForm(plateMap, libraryFilter, lib_form_element, user_selector);
	populateCopyForm(plateMap);
}



function createLibCopyRegGUI(parent_element, plateMap)
{
	$td_lib_form = $('<td>', {
		
		id: "td_lib_form",
		class: "td_reg_flow"
	});
	
	parent_element.append($td_lib_form);	
	
		$div_lib_form = $('<div>', {
			id : "div_lib_form",
		});
		
		$td_lib_form.append($div_lib_form);
		
		
		
	$td_lead0 = $('<td>', {
	
		id: "td_lead0",
		class: "td_reg_flow_lead",
	});
	
	parent_element.append($td_lead0);
	
		$img_lead0 = $('<img>', {
		
			id: "img_lead0",
			src : "/static/yeast_libraries/img/lead.png",
		});
	
		$td_lead0.append($img_lead0);
			
			
			
	$td_copy_form = $('<td>', {
		
		id: "td_copy_form",
		class: "td_reg_flow",
	});
	
	parent_element.append($td_copy_form);	
	
		$div_copy_form = $('<div>', {
			id : "div_copy_form",
		});
		
		$td_copy_form.append($div_copy_form);
		
		
	createLibFilter(parent_element, plateMap);
}



function populateLibForm(plateMap, libraryFilter, parent_element, selector)
{
	this.selector = selector;
	
	this.update = function () 
	{
		//console.log('libRegisterCallback');
		
		//console.log('JSON.stringify(plateMap): ', JSON.stringify(plateMap));
		//console.log('hufflepuff');
		
		plateMap.getMap([ALL_NICKNAMES], true, updatePlateChoosingGUI, true);
		
		
		//console.log('$s_users.val(): ', $s_users.val());
		
		var nicknames = [ALL_NICKNAMES];
		
		if($s_users.val())
		{
			nicknames = $s_users.val();
		}
		
		copyRegister.getAndDisplayDataFromServer(nicknames);
		
		libraryFilter.getMap(this.selector);
		// $div_msg.empty();
		// $div_msg.append('<h1>' + this.responseText + '<h1>');
	};
	
	createLibraryRegisterForm(parent_element, this.update);
}



function populateCopyForm(plateMap)
{
	copyRegister = new CopyRegister(copyRegisterCallback, plateMap);
	copyRegister.createRegisterStackGUI($div_copy_form);
	
	//console.log('2 $s_users.val(): ', $s_users.val());
	
	var nicknames = [ALL_NICKNAMES];
		
	if($s_users.val())
	{
		nicknames = $s_users.val();
	}
	
	copyRegister.getAndDisplayDataFromServer(nicknames);
	
	
}

function copyRegisterCallback(plateMap, responseText) 
{
	
	console.log('copyRegisterCallback');
	console.log('responseText: ', responseText);
	
	//console.log('JSON.stringify(plateMap): ', JSON.stringify(plateMap));
	
	//console.log('plateMap.focusedPlate');
	
	var nicknames = [ALL_NICKNAMES];
		
	if($s_users.val())
	{
		nicknames = $s_users.val();
	}
	
	var is_liquid = true;
	
	if(plateMap.context_view == MAIN_CONTEXT)
	{
		var is_liquid = false;
	}
	
	 
	
	plateMap.getMap(nicknames, is_liquid, updatePlateChoosingGUI, true);
}



