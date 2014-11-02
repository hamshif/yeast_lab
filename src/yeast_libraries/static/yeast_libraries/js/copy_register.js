

function CopyRegister(callback, plateMap)
{
	//console.log(plateMap.context_view);
	
	this.callback = callback;
	this.plateMap = plateMap;
	this.map;
	this.focused_library;
	this.focused_stack;
	this.parent_stack;

	var cr = this;
	
	this.postForm = function ()
	{
		//console.log('postForm()');
		
		tellUser('Please Wait');
		// $div_msg.empty();
		// $div_msg.append('<h1>uploading wait for message or browse<h1>');
		var formData = new FormData();
		
		
		//library = getSelectedText('select_library');
		var library = $select_library.prop('value');
		//console.log('library: ', library);
		formData.append('library', library);
		
		var stack = $select_stack.prop('value');
		//console.log('stack: ', stack);
		formData.append('stack', stack);
		
		var medium = $select_stack_form_medium.prop('value');
		//console.log('medium: ', medium);
		formData.append('medium', medium);
		
		var storage = $select_stack_form_storage_name.prop('value');
		//console.log('storage: ', storage);
		formData.append('storage', storage);
		
		
		var time = $('#datetimepicker4').val();
		//console.log('time: ', time);
		formData.append('time', time);
	
		var is_liquid = $cb_is_liquid.prop('checked');
		//console.log('is_liquid: ', is_liquid);
		formData.append('is_liquid', is_liquid); 
		
		var comments = $('#ta_stack_form_comments').val();
		//console.log('comments: ', comments);
		formData.append('comments', comments);
		
		
		
		var xhr = new XMLHttpRequest();
		xhr.onload = localCallback;
		xhr.open('POST', "/yeast_libraries/stack_register/", true);
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
		console.log(xhr);
		
		xhr.send(formData);
	};

	function localCallback()
	{
		console.log('localcallback');
		
		var j = JSON.parse(this.responseText);
		
		console.log('JSON.parse(this.responseText): ', j);
		
		if(typeof j['error'] == 'undefined')
		{
			
			var copy = j['new_stack'];
			var l = j['library_name'];
			var name1 = copy['name'];
			
			tellUser(name1 + ' successfuly registered');
			
			cr.map[l]['stacks'][name1] = copy; 
			
			$select_library.empty();
			$select_stack.empty();
			cr.populateLibStackMaps();
			
			console.log('cr.plateMap: ', cr.plateMap);
			
			cr.callback(cr.plateMap, j);
		}
		else
		{
			tellUser(j['error']);
		}
	}


	function tellUser(text)
	{
		$p_copy_mesage.empty();
		$p_copy_mesage.append('<p>' + text + '</p>');
	}
	


	this.createRegisterStackGUI = function (parent_element)
	{	
		//console.log('parent_element', parent_element);
		
		parent_element.append('<h1>Register New Copy</h1>');
		
		$t_copy_form = $('<table>', {
			id: 't_copy_form',
		});
		
		parent_element.append($t_copy_form);
		
			$tr_copy_form1 = $('<tr>', {
				id: "tr_copy_form1",
			});
			
			$t_copy_form.append($tr_copy_form1);
			
				$td_cf1 = $('<td>', {
					id: 'td_cf1',
				});
				
				$tr_copy_form1.append($td_cf1);
				
					$h_stack_form_library_name = $('<h2>Library Type</h2>');
					$td_cf1.append($h_stack_form_library_name);
					$select_library = $('<select name="library" id="select_library" multiple></select multiple>');
					$td_cf1.append($select_library);
					
					$td_cf1.append('<h2>Check for Liquid Copy<h2>');
					
					$cb_is_liquid = $('<input id="cb_is_liquid", type="checkbox", name= "is_liquid"></input>');
					
					$td_cf1.append($cb_is_liquid);
	
					if(this.plateMap.context_view == 'liquid_plate_analysis')
					{
						$cb_is_liquid.prop('checked', true);
					}
	
					$h_stack_form_stack_name = $('<h2>Origin Stack (copy)</h2>');
					$td_cf1.append($h_stack_form_stack_name);
					$select_stack = $('<select name="stack" id="select_stack" multiple></select multiple>');
					$td_cf1.append($select_stack);
					
					$td_cf1.append('<h2>Time Of Actual Copying</h2>');
					$it_stack_form_time = $('<input name="time" type="text" value="2014/2/03 12:00" id="datetimepicker4"/><input id="open" type="button" value="set time"/><input id="close" type="button" value="close"/><input id="reset" type="button" value="reset"/>');
					$td_cf1.append($it_stack_form_time);
					
			
				$td_cf2 = $('<td>', {
					id: 'td_cf2',
				});
				
				$tr_copy_form1.append($td_cf2);
			
					
					$h_stack_form_medium = $('<h2>Medium</h2>');
					$td_cf2.append($h_stack_form_medium);
					$select_stack_form_medium = $('<select name="medium" id="select_stack_form_medium" multiple></select multiple>');
					$td_cf2.append($select_stack_form_medium);
					
					$td_cf2.append('<h2>Comments</h2>');
					$ta_stack_form_comments = $('<textarea cols="40", rows="5", name="comments", id ="ta_stack_form_comments"></textarea>');
					$td_cf2.append($ta_stack_form_comments);
					
					
					$td_cf2.append('<h2>Storage</h2>');	
					$select_stack_form_storage_name = $('<select name="storage" id="select_stack_form_storage_name" multiple></select multiple>');
					$td_cf2.append($select_stack_form_storage_name);
					
					
					$td_cf2.append('<h2></h2>');
				
					$('#datetimepicker4').datetimepicker();
					$('#open').click(function(){
						$('#datetimepicker4').datetimepicker('show');
					});
					$('#close').click(function(){
						$('#datetimepicker4').datetimepicker('hide');
					});
					$('#reset').click(function(){
						$('#datetimepicker4').datetimepicker('reset');
					});
					
		
		$p_copy_mesage = $('<p>', {
			id: "p_copy_mesage",
			text: "Message",
			class: "progress_message",
		});			
		parent_element.append($p_copy_mesage);			
					
		$b_submit_stack_form = '<input id="b_submit_stack_form" type="button" value="submit library copy"/>';
		parent_element.append($b_submit_stack_form);
		$('#b_submit_stack_form').click(function()
		{
			cr.postForm();
		});
	};
	
	
	this.getAndDisplayDataFromServer = function (nicknames)
	{
		//console.log('getAndDisplayDataFromServer: ');
		
		var j = {'nicknames': nicknames};	
		//console.log('JSON.stringify(j): ', JSON.stringify(j));	
		//console.log('csrftoken: ', csrftoken);	
		
		$.ajax({
		    url: '/yeast_libraries/lib_stack_map/',
		    type: 'POST',
		    contentType: 'application/json; charset=utf-8',
		    data: JSON.stringify(j),
		    //data: experiment,
		    dataType: 'json',
		    
		    beforeSend: function(xhr) {
				//console.log('xhr', xhr);
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
		    success: function(json) 
			{
				  //console.log('response: /yeast_libraries/lib_stack_map/:');
				  
				  //console.log('JSON get response: ', JSON.stringify(json));	  
				  
				  var j_mediums = json['mediums'];
				  //console.log('mediums: ', j_mediums);
				  populateMediums(j_mediums);
				  	  
				  
				  var j_storages = json['storages'];
				  //console.log('storages: ', j_storages);
				  populateStorages(j_storages);
		 
				  
				  cr.map = json['lib_stack_map'];
				  //console.log('JSON.stringify(cr.map): ');
				  //console.log(JSON.stringify(cr.map));
				    
				  cr.populateLibStackMaps();
			},
		});	
	};
	
	
	populateMediums = function(j_mediums)
	{
		$('#select_stack_form_medium').empty();
		
		for(key in j_mediums)
		{
	  	  	// medium = j_mediums[j_medium];
	  		//console.log('        medium: ', key);
	  	  	var medium = j_mediums[key];
	  	  	//console.log('medium:', medium);
	  	  	o = new Option(key, medium['primary_key']);
	  	    
		  	$select_stack_form_medium.append(o);	
	  	}
	  
	  	if(Object.keys(j_mediums).length > 0);
	  	{
	  		$('#select_stack_form_medium option').eq(0).prop('selected', true);
	  	}
	};
	
	
	populateStorages = function(j_storages)
	{
		$('#select_stack_form_storage_name').empty();
		
		for(j_storage in j_storages)
	  	{
	  	  	var storage = j_storages[j_storage];
	  	  	//console.log('        storage: ', storage);
	  		o = new Option("option text", storage);
	  	    
	  	  	$(o).html(storage);
		  	$select_stack_form_storage_name.append(o);	
	  	}
	  
	  	if(Object.keys(j_storages).length > 0);
	  	{
	  		$('#select_stack_form_storage_name option').eq(0).prop('selected', true);
	  	}
	};
	
	
	this.populateLibStackMaps = function ()
	{
		//console.log('JSON.stringify(cr.map): ', JSON.stringify(cr.map));
		$('#select_library').empty();
	
		for(key in cr.map)
		{
			stacks = cr.map[key]['stacks'];
			l_pk = 	cr.map[key]['pk'];		
			
			//console.log('l_pk: ', l_pk);
			
			o = new Option(key, l_pk);
			  
			$(o).bind('click', function()
			{	
				//console.log('clicked!!!');
				
				this.focused_library = 	$("#select_library option:selected").text();
				
				//console.log('this.focused_library: ', this.focused_library);
				//$select_stack_form_library_name.val( focused_lib_name ).prop('selected',true);		
				
				if(this.focused_library != -1)
				{
					stacks = cr.map[this.focused_library]['stacks'];
					
					$select_stack.empty();
				  	
				  	o1 = new Option('none', 0);
					    	
			    	$(o1).bind('click', function()
					{	
						focused_stack = getSelectedText('select_stack');
					});
					
					$select_stack.append(o1);
				  	
				  	
				  	if(Object.keys(stacks).length != 0)
				    {
				    	for(key in stacks)
					    {
							//console.log('  key: ', stacks[key]);
					    	
					    	s_pk = stacks[key]['pk'];
					    	s_name = stacks[key]['name'];
					    	
					    	o1 = new Option(s_name, s_pk);
					    	
					    	$(o1).bind('click', function()
							{	
								focused_stack = getSelectedText('select_stack');
							});
					    	
				  			$select_stack.append(o1);
					    }
				    }
				 }
				 else
				 {
				   	$select_stack.empty();
				 }
			});
			
			$select_library.append(o);	
			
			
			if(stacks.length == 0)
			{
				//console.log('      stack:', 'none');
			}
			else
			{
				$('#select_stack option').eq(0).prop('selected', true);	
			}		  
		
		}//end of for(key in j_snapshot_map)
	
	    $('#select_library option').eq(0).prop('selected', true);
	    $('#select_library option').eq(0).click();
	    
	    if($('#select_library option').eq(0).size() > 0)
	    {
	    	$('#select_stack option').eq(0).prop('selected', true); 
	    	$('#select_stack option').eq(0).click();
	    }
	};
}




