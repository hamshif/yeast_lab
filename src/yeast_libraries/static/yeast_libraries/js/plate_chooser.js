

function PlateMap(context_view)
{
	this.context_view = context_view;
	this.map;
	this.focused_lib_name;
	this.focused_stack_name;
	this.total_plates;
  	this.focused_plate;
  	this.dataMap;

	var plateMap = this;
	
	this.getMap = function (nicknames, is_liquid, update, justMap)
	{
		//console.log('nicknames: ', nicknames);
		//console.log('PlateMap.getMap()');		
		var j = {'nicknames': nicknames, 'is_liquid': is_liquid};	
		//console.log('j', j);
		
		//console.log('csrftoken: ', csrftoken);	
		
		$.ajax({
		    url: '/yeast_libraries/plate_map/',
		    type: 'POST',
		    contentType: 'application/json; charset=utf-8',
		    data: JSON.stringify(j),
		    //data: experiment,
		    dataType: 'json',
		    
		    beforeSend: function(xhr) {
				//console.log('xhr', xhr);
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
		    
		    
		    success: function(data) 
			{
				  // console.log('response /yeast_libraries/plate_map/: ');
				  // console.log(JSON.stringify(data));
				  plateMap.map = data;//JSON.parse(data);	
				  //console.log('chork');
				  if(justMap == undefined)
				  {
				  	plateMap.initiate();
				  	//console.log('initiated all fields');
				  }
				  else
				  {
				  	//console.log('initiated just map');
				  }
				  
				  //console.log('plateMap.focused_lib_name: ', plateMap.focused_lib_name);
				  //console.log('flamboyant');
				  update(plateMap);
			},
		});	
		
	};
	
	

	this.initiate = function ()
	{
		var lib_keys = Object.keys(plateMap.map);
		
		if(lib_keys.length > 0)
		{
			plateMap.focused_lib_name = lib_keys[0];
		}
		else
		{
			//console.log('no libraries');
			return false;
		}
	 	
		
		var copy_keys = Object.keys(plateMap.map[plateMap.focused_lib_name]['stacks']);
		
		if(copy_keys.length > 0)
		{
			plateMap.focused_stack_name = copy_keys[0];
		}
		else
		{
			//console.log('no copies');
			return false;
		}		
	 	
	 	
	 	//console.log('context', this.context_view, 'found copies');
	 	return true;
	};
	
	this.setDataMap = function (dataMap)
	{
		plateMap.dataMap = dataMap;
	};
	
	
	this.nextPlate = function (update)
	{	
		if(plateMap.total_plates > plateMap.focused_plate)
		{
			plateMap.focused_plate++;
		}
		else
		{
			plateMap.focused_plate = 0;
		}	
		
		update(plateMap);
	};
	
	
	this.backPlate = function (update)
	{	
		if(plateMap.focused_plate > 0)
		{
			plateMap.focused_plate--;
		}
		else
		{
			plateMap.focused_plate = plateMap.total_plates;
		}
		
		update(plateMap);
	};
	
	
	this.setAll = function(lib_id, copy_id, plate_id, update)
	{
		console.log('JSON.stringify(plateMap.map): ', JSON.stringify(plateMap.map));
		
		for(var lib_name in plateMap.map)
		{
			var lib = plateMap.map[lib_name];
			
			if(lib_id == lib['pk'])
			{
				for(var stack_name in lib['stacks'])
				{
					var stack = lib['stacks'][stack_name]; 
					
					if(copy_id == stack['pk'])
					{
						var plates = stack['plates'];
						
						for(var plate_pk in plates)
						{
							var plate = plates[plate_pk];
							
							console.log("JSON.stringify(plate): ", JSON.stringify(plate));
							console.log('plate_id: ', plate_id , "   plate['pk']: ", plate['pk'] + '');
							
							if(plate_id == plate['pk'] + '')
							{
								console.log('wooo');
								
								plateMap.setLib(lib_name, stack_name, plate['index'] -1);
								update(plateMap);
								
								break;
							}
						}
						
						break;
					}
				}
				
				break;
			}
		}
	};
	
	
	
	
	this.setLib = function (lib_name, stack_name, plate_index)
	{	
		var lib_keys = Object.keys(plateMap.map);
		
		if(lib_keys.length > 0)
		{
			if(lib_name === undefined)
			{
				plateMap.focused_lib_name = lib_keys[0];
			}
			else
			{
				plateMap.focused_lib_name = lib_name;
			}
		}
		else
		{
			plateMap.focused_lib_name = undefined;
			plateMap.focused_stack_name = undefined;
			plateMap.total_plates = undefined;
			plateMap.focused_plate = undefined;
			console.log('no libraries');
			return false;
		}
		
		return(plateMap.setStack(stack_name, plate_index));
	};
	
	this.setStack = function (stack_name, plate_index)
	{		
		var copy_keys = Object.keys(plateMap.map[plateMap.focused_lib_name]['stacks']);
		
		if(copy_keys.length > 0)
		{
			//console.log(copy_keys.length, ' copies');
			
			
			if(stack_name === undefined)
			{
				plateMap.focused_stack_name = copy_keys[0];
			}
			else
			{
				plateMap.focused_stack_name = stack_name;
			}
		}
		else
		{
			plateMap.focused_stack_name = undefined;
			plateMap.total_plates = undefined;
			plateMap.focused_plate = undefined;
			console.log('no copies');
			return false;
		}
	 	
	 	//console.log('plateMap.focused_stack_name:', plateMap.focused_stack_name);
	 	if(plate_index == undefined)
	 	{
	 		plate_index = 0;
	 	}
	 	
	 	return plateMap.setPlate(plate_index);
	};
	
	
	this.setPlate = function(index)
	{
		var plates = plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['plates'];
		
		plateMap.total_plates = plates.length - 1;
		
		if(plateMap.total_plates > 0)
		{
			if(index < plateMap.total_plates)
			{
				plateMap.focused_plate = index;
			}
			else
			{
				plateMap.focused_plate = 0;
			}
		}
		else
		{
			plateMap.focused_plate = undefined;
			console.log('no plates');
			return false;
		}
		
		// console.log('plateMap.total_plates:', plateMap.total_plates);
		// console.log('plateMap.focused_plate:', plateMap.focused_plate);
	 	
	 	return true;	
	};
}


PlateMap.prototype.getFocusedPlateID = function()
{
	var plate_id = this.map[this.focused_lib_name]['stacks'][this.focused_stack_name]['plates'][this.focused_plate]['pk'];
	return plate_id;
};

PlateMap.prototype.getFocusedCopyID = function()
{
	var copy_id = this.map[this.focused_lib_name]['stacks'][this.focused_stack_name]['pk'];
	return copy_id;
};


function populatePlateChooser(plateMap, update, lib_selector, copy_selector, promptCopyRegister)
{
	lib_selector.empty();
	copy_selector.empty();
	$plate_counter.html('No Plates Chosen');
	
	if(plateMap.focused_lib_name != undefined)
	{
		for(var key in plateMap.map)
		{	
			var l_pk = 	plateMap.map[key]['pk'];	
			var o = new Option(key, l_pk);
			  
			$(o).bind('click', function()
			{					
				plateMap.setLib(this.text);
				
				//console.log(plateMap.focused_lib_name, plateMap.focused_stack_name);
				
				var stacks = plateMap.map[plateMap.focused_lib_name]['stacks'];
// 				
				// console.log('JSON.stringify(stacks):');
				// console.log(JSON.stringify(stacks));
				
				copy_selector.empty();
			  	
			  	var stacks_length = Object.keys(stacks).length;
			  	
			  	if(stacks_length == 0)
			    {
			    	promptCopyRegister(plateMap);
			    }
			    else
			    {
			    	var ordered_stacks = plateMap.map[plateMap.focused_lib_name]['ordered_copy_keys'];
					// console.log('ordered_stacks:');
					// console.log(ordered_stacks);


				    for(var j in ordered_stacks)
				    {
				    	var key1 = ordered_stacks[j];
				    	
				    	//console.log(key1);
				    	
				    	var s_pk = stacks[key1]['pk'];
				    	var s_name = stacks[key1]['name'];
				    	
				    	var o1 = new Option(s_name, s_pk);
				    	
				    	$(o1).bind('click', function()
						{	
							plateMap.setStack(stacks['name']);
							//console.log('context', plateMap.context_view, 'copy option', this.text, 'clicked');							
							
							plateMap.setStack(this.text);
							update(plateMap);
						});
				    	
				    	$(o1).html(key1);
			  			copy_selector.append(o1);
				    }
				    
				    //$('#stack_list option').eq(stacks_length - 1).prop('selected', true); 
				    copy_selector.get(0).options[stacks_length - 1].selected = true;
    				copy_selector.get(0).options[stacks_length - 1].click();
			    }
				 
			});
				 
			$(o).html(key);
			lib_selector.append(o);	
		}

	    //$('#library_list option').eq(0).prop('selected', true);
	    
	    
	    //lib_selector.get(0).options[0].selected = true;
	    
	    //lib_selector.get(0).options[0].click();
	    
	    // if(lib_selector.get(0).options.length > 0)
	    // {
	    	// if(copy_selector.get(0).options.length > 0)
	    	// {
	    		// copy_selector.get(0).options[0].selected = true;
	    		// copy_selector.get(0).options[0].click(); 
	    	// }
		    // else
			// {
				// copy_selector.empty();
			// }
	    // }
	    // else
		// {
			// lib_selector.empty();
			// copy_selector.empty();
		// }
	}
	else
	{
		lib_selector.empty();
		copy_selector.empty();
	}
}

function updatePlateGUI(plateMap)
{
	//console.log('updatePlateGUI');
	var copy_selector = $('#stack_list');;
	var plate_counter = $plate_counter;
	
	
	//console.log('plateMap.context_view: ', plateMap.context_view);
	
	if(plateMap.context_view == 'compared')//)
	{
		copy_selector = $('#compared_stack_list');
		plate_counter = $compared_plate_counter;
	}
	
	
	if(plateMap.context_view != 'liquid_plate_analysis')
	{
		clearAnalysis();
	}
	
	if(plateMap.focused_plate == undefined)
	{
		plate_counter.html('No Plates');
	}
	else
	{
		plate_counter.html('Plate # ' + (plateMap.focused_plate + 1) + ' of ' + (plateMap.total_plates + 1));
	}

	
}

// function promptCopyRegister()
// {
	// if(confirm(plateMap.focused_lib_name + ' Library/Plate Has no registered copies!\nDo Yo want to register a copy?'))
	// {
		// console.log('need to redo');
// 		
		// if(plateMap.context_view == 'liquid_plate_analysis')
		// {
			// $b_register_copy.click();
		// }
		// else
		// {
			// window.location.href = '/yeast_libraries/stack_register_gui/';
		// }
	// }
// }




