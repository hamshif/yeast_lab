
var available_plates;
var selected_plate;
var csrftoken;


var platePattern;
var experimentChooser;
var plateExperimentChooser;


$(document).ready(function()
{
	csrftoken = getCookie('csrftoken');
	//console.log('csrftoken: ', csrftoken);
	
	var plateMap = new PlateMap(LIQUID_CONTEXT);
	experimentChooser = new ExperimentChooser(LIQUID_CONTEXT, plateMap);
	platePattern = new PlatePattern();
	
	libraryFilter = new LibraryFilter(plateMap);
	
	createGUI(plateMap, libraryFilter, experimentChooser);
	getAvailablePlates();
	
	plateMap.getMap([ALL_NICKNAMES], true, updatePlateChoosingGUI);
	
	libraryFilter.getMap($s_users);
	
	experimentChooser.getExperiments(COMMON_USER, experimentClicked);	
});


experimentClicked = function (experiment, plateMap)
{
	console.log('experimentClicked');
	console.log("JSON.stringify(experiment): ", JSON.stringify(experiment));
	plateMap.setAll(experiment['lib_id'], experiment['copy_id'], experiment['plate_id'], plateChange);
};


function updatePlateChoosingGUI(plateMap)
{
//	console.log('updatePlateChoosingGUI');
	populatePlateChooser(plateMap, plateChange , $('#library_list'), $('#stack_list'), promptCopyRegister); 
	
	var nicknames = $s_users.val();
			
	if(!nicknames)
	{
		nicknames = ALL_NICKNAMES;
	}
	
	copyRegister.getAndDisplayDataFromServer(nicknames);
}

function promptCopyRegister(plateMap)
{
	console.log('promptCopyRegister');
	
	createCellChooser(undefined, $div_cell_chooser); 
	
	
	if(confirm(plateMap.focused_lib_name + ' does not have registered copies! Want to register one?'))
	{
		$b_new_data.click();
	}
}



function updateNextPlateGUI(plateMap)
{
	$plate_counter.html('Plate # ' + plateMap.current_plate.toString() + ' of ' + plateMap.total_plates.toString());
}


function updateCellChooser(plateMap)
{
	var plate_pk = plateMap.getFocusedPlateID();
	var copy_pk = plateMap.getFocusedCopyID();

//    console.log('plateMap: ', plateMap);
//    console.log('plate_pk: ', plate_pk);

	platePattern.getMap(copy_pk, plate_pk, updateCellChooserGUI);
}



function getAvailablePlates()
{
	// console.log('getAvailablePlates()');
	
	$.ajax
	(
		{ 
			url: "/yeast_liquid_plates/get_available_liquid_plates", 
			success: function(response)
			{
				//console.log('response: /yeast_liquid_plates/get_available_liquid_plates', response);
				available_plates = JSON.parse(response);
				
				for(i=0; i < available_plates.length; i++)
				{	
					plate = available_plates[i];
					
					$select_data.append(
						$('<option>',{
						value : plate,
						text : plate,
						click: function(){ selectPlate(this.text);}
						})
					);
				}
				
			}
		}

	);
}

function createGUI(plateMap, libraryFilter, experimentChooser)
{
	//console.log('createGUI()');
	
	$div_new_data_control = $('<div>', {
		id:"div_new_data_control", 
		class:"new_data_choice_control"
	});
	
	$('body').append($div_new_data_control);
	
	
	$div_reg = $('<div>', {
		id:"div_reg"
	});
	
	$('body').append($div_reg);
	
	
	$div_choose = $('<div>', {
		id:"div_choose"
	});
	
	$('body').append($div_choose);

    $div_plot = $('<div>', {
		id:"div_plot"
	});

	$('body').append($div_plot);
    $div_plot.show();
	
	
	//$div_reg_control.hide();
	$div_reg.hide();
	$div_choose.hide();
	
	
	$t_new_data_control = $('<table>', {
		id: 't_new_data_control',
		class : "new_data_choice_control"
	});
	
	
	$div_new_data_control.append($t_new_data_control);
	
		$tr_new_data_control = $('<tr>',{
			id: 'tr_new_data_control'
		});
	
		$t_new_data_control.append($tr_new_data_control);
	
	
	$t_forms = $('<table>', {
		id: "t_forms"
	});	
	
	$div_reg.append($t_forms);
	
	$t_choice = $('<table>', {
		id: "t_choice"
	});
	
	$div_choose.append($t_choice);
	
	
		$tr_reg_flow = $('<tr>', {
			id : "tr_reg_flow"
		});

		$t_forms.append($tr_reg_flow);
	
	
	
		$tr_flow1 = $('<tr>', {
			id : "tr_flow1"
		});

		$t_choice.append($tr_flow1);
		
		$tr_flow2 = $('<tr>', {
			id : "tr_flow2"
		});

		$t_choice.append($tr_flow2);
		
	
	
	createNewDataChoice();
	
	createLibCopyRegGUI($tr_reg_flow, plateMap);
	populateLibCopyGUI(plateMap, libraryFilter, $tr_flow1, $div_lib_form, $s_users);
	
	createDataChoice(plateMap, experimentChooser);
	createExperimentChoice(experimentChooser);
	
	createPlateChoice(plateMap);
	
	
		
	
	
	$td_cell_chooser = $('<td>', {
		
		id: "td_cell_chooser"
	});
	
	$tr_flow1.append($td_cell_chooser);	
	
	
		$div_cell_chooser = $("<div>", {
			
			id: "div_cell_chooser"
			
		});
	
		$td_cell_chooser.append($div_cell_chooser);
		
		createCellChooser(undefined, $div_cell_chooser);
	
		
		$div_growth_getter = $('<div>', {
			
			id: 'div_growth_getter',
			class: "growth_getter"
		});
		
		$('body').append($div_growth_getter);
		
		//$div_wrap_growth_getter.append($div_growth_getter);	
			
			$div_growth_getter.append('<h2 id="h_focused_experiment" >Focused Experiment</h2>');
			
			$b_get_growth = $('<input>', {
				
				id: "b_get_growth",
				type:"button",
				value: "Get Growth",
				click: function()
					{
						platePattern.getCellsGrowth(); 
					}
			});
			
			$div_growth_getter.append($b_get_growth);
			
	$div_growth_getter.hide();
			
			// var html_org =  $('#h_focused_experiment').html();
			// var html_calc = '<span>' + html_org + '</span>';
			// $('#h_focused_experiment').html(html_calc);
// 			
			// console.log('Batata!!!', $('#h_focused_experiment').find('span:first').width());
// 			
			// $div_growth_getter.width($('#h_focused_experiment').find('span:first').width() + 20);
}



function createNewDataChoice()
{
	$td_show_all = $('<td>', {
		
		id: "td_show_all",
		style:"vertical-align:top;",
		class: 'stam'
		
	});
	
	$tr_new_data_control.append($td_show_all);

		$b_show_all = $('<input>', {
			id : "b_show_all",
			type : "button",
			click : function()
			{
				console.log(this.value);
				$div_choose.show();
				$div_reg.show();
				$td_cell_chooser.show();
				$div_growth_getter.show();
			},
			value: "Show All",
			class: "b_major_choice"
		});
		
		$td_show_all.append($b_show_all);
		
		$td_show_all.hide();
	
	
	$td_new_data = $('<td>', {
		
		id: "td_new_data",
		style:"vertical-align:top;",
		class: 'stam'
		
	});
	
	$tr_new_data_control.append($td_new_data);

		$b_new_data = $('<input>', {
			id : "b_new_data",
			type : "button",
			click : function()
			{
				console.log(this.value);
				//$div_reg_control.show();
				$div_reg.show();
				$div_choose.hide();
				$div_growth_getter.hide();
				$('.b_major_choice').toggleClass('b_major_choice b_minor_choice');
				$('.new_data_choice_control').toggleClass('new_data_choice_control new_data_choice_control_small');
				$td_show_all.show();
				
				$td_experiment_choice.appendTo($tr_reg_flow);
				$td_search.appendTo($tr_reg_flow);
				$td_plate_choice.appendTo($tr_reg_flow);
			},
			value: "New Data",
			class: "b_major_choice"
		});
		
		$td_new_data.append($b_new_data);
		
		
	$td_known_data = $('<td>', {
		
		id: "td_known_data"
	});
	
	$tr_new_data_control.append($td_known_data);

		$b_known_data = $('<input>', {
			id : "b_known_data",
			type : "button",
			click : function()
			{
				//console.log(this.value);
				$div_choose.show();
				$div_reg.hide();
				$div_growth_getter.show();
				//$div_reg_control.show();
				$('.b_major_choice').toggleClass('b_major_choice b_minor_choice');
				$('.new_data_choice_control').toggleClass('new_data_choice_control new_data_choice_control_small');
				$td_show_all.show();
				
				$td_experiment_choice.appendTo($tr_flow1);
				$td_search.appendTo($tr_flow1);
				$td_plate_choice.appendTo($tr_flow1);
				$td_cell_chooser.appendTo($tr_flow1);
			},
			value: "Registered Data",
			class: "b_major_choice"
		});
		
		$td_known_data.append($b_known_data);
}





function createExperimentChoice(experimentChooser)
{		
	this.experimentChooser = experimentChooser;
	$td_experiment_choice = $('<td>', {
		
		id: "td_experiment_choice",
		class: "td_reg_flow"
	});
	
	$tr_flow1.append($td_experiment_choice);	
	
		$div_experiment_choice = $('<div>', {
			id : "div_experiment_choice"
		});
		
		$td_experiment_choice.append($div_experiment_choice);
	
	experimentChooser.createChooserGUI($div_experiment_choice);
}



function affiliateDataToPlate(plateMap, experimentChooser)
{
	//console.log("affiliateDataToPlate()");
	
	if(selected_plate === undefined)
	{
		alert('Please choose data');
		return;
	}
	
	//console.log(plateMap.current_plate);
	
	if(plateMap.focused_plate === undefined)
	{
		alert('Please choose a plate to affiliate data');
		return;
	}
	
	//console.log(JSON.stringify(plateMap.map));
	console.log('     Focused Plate JSON');
	console.log(JSON.stringify(plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['plates'][plateMap.focused_plate]));
	var plate_pk = plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['plates'][plateMap.focused_plate]['pk'];	
	
	var j = "plate_data_dir="+ selected_plate + "&plate_pk=" + plate_pk;
	
	console.log('query: ', j);
	
	$.ajax({
	  type: "POST",
	  url: "/yeast_liquid_plates/affiliate_data_to_plate/?" + j,
	  //data: '{ plate: John, data: Boston }',
	  success: function (msg)
	  {
	  	console.log( "response /yeast_liquid_plates/affiliate_data_to_plate/: " + msg );
	  	var j = JSON.parse(msg);
	  	
	  	var status = j['status'];
	  	
		if(status == 'error')
		{
			console.log('error:',   j['message']);
			$p_data_affiliation_progress_message.empty();
			$p_data_affiliation_progress_message.append('<p>' + j['message'] + '</p>');
		}
		else
		{
			$p_data_affiliation_progress_message.empty();
			$p_data_affiliation_progress_message.append('<p>' + 'Your request is registered. We are reading the experiment data and will notify you of progress 0' + '</p>');
			
		  	var request_params  = ''.concat('process_pk=', j['process_pk']);
		  	affiliateFollowup(request_params, experimentChooser, 0);
		}
	  }
	});

}

function affiliateFollowup(request_params, experimentChooser, repeat)
{
	console.log('affiliateFollowup...');
	
	console.log('experimentChooser: ', experimentChooser);
	
	$.ajax
	(
		{ 
			url: "/yeast_liquid_plates/affiliate_follow_up/", 
			data: request_params,
			experimentChooser: experimentChooser,
			success: function(response)
			{
				console.log('/yeast_liquid_plates/affiliate_follow_up/: ', response);
				
				var j_dict = JSON.parse(response);
				console.log('j_dict: ', j_dict);
				
				var process_pk = j_dict['process_pk'];
				var status = j_dict['status'];
				
				console.log('status: ', status);
				
				
				var request_params  = ''.concat('process_pk=', process_pk);
				
				
				console.log('time after timeout', new Date().getTime());
				console.log('request_params: ', request_params);
				
				if(status == "bussy")
				{
					checkAffiliateStatus(request_params, experimentChooser, repeat + 1);
					
					
					
					var msg = $p_data_affiliation_progress_message.text();
					
					msg = msg.slice(0,-2) + " " + repeat;
					
					console.log('msg: ', msg);
					
					$p_data_affiliation_progress_message.empty();
					$p_data_affiliation_progress_message.append('<p>' + msg + '</p>');
				}
				else
				{
					//console.log('total folowup time', new Date().getTime() - t_snap_debug);
					console.log('Mupitzee');
					var experiment = j_dict['experiment'];
					experimentChooser.addExperiments(experiment);
					
					$p_data_affiliation_progress_message.empty();
					$p_data_affiliation_progress_message.append('<p>' + 'Success' + '</p>');
					
					$b_known_data.click();
				}
					
			}
		}
	);
}

function checkAffiliateStatus(request_params, experimentChooser, repeat)
{
	console.log('dealWithSnapshotFollowup...');
	console.log('request_params: ', request_params);
	//clearTimeout(timeoutId);
	
	//timeoutId = setTimeout
	console.log('settimeout', setTimeout
	(	
		function(){affiliateFollowup(request_params, experimentChooser, repeat);},
		10000
	));
	
		  // $.each(document.cookie.split(/; */), function()  {
	  // var splitCookie = this.split('=');
	  // console.log('key: ', splitCookie[0], '  value is: ', splitCookie[1]);
	// });
}



function createDataChoice(plateMap, experimentChooser)
{
	$td_lead = $('<td>', {
		
		id: "td_lead",
		class: "td_reg_flow_lead"
	});
	
	$tr_reg_flow.append($td_lead);
	
		$img_lead = $('<img>', {
		
			id: "img_lead",
			src : "/static/yeast_libraries/img/lead.png"
		});
	
		$td_lead.append($img_lead);
	
	
	
	$td_data_choice = $('<td>', {
		
		id: "td_data_choice",
		class: "td_reg_flow"
	});
	
	$tr_reg_flow.append($td_data_choice);
	
		$div_data = $('<div>', {
			id : "div_data"
		});
		
		$td_data_choice.append($div_data);
		
			$div_data.append('<h1>Data</h1>');
			
			$div_data.append('<h2>Directories</h2>');
		
			$select_data = $('<select multiple>', {
				id: "select_data"
			});
			
			$div_data.append($select_data);
			
			$div_data.append('<br>');
			
			$b_submit_liquid = $('<input>', {
			
				id: "b_submit_liquid",
				type:"button",
				value: "Affiliate Data With Plate",
				click: function(){affiliateDataToPlate(plateMap, experimentChooser);}
			});
			
			$div_data.append($b_submit_liquid);
			
			$p_data_affiliation_progress_message = $('<p>',{
			
				id: "p_data_affiliation_progress_message",
				class: "progress_message",
				text: "Progress Message"
			});
			
			$div_data.append($p_data_affiliation_progress_message);
}






function selectPlate(plate)
{
	selected_plate = plate;
	//console.log('selected_plate: ', selected_plate);	
}

function getRawFile()
{
	if(selected_plate === undefined)
	{
		alert('Please choose a plate first');
		return;
	}
	
	location.href="/yeast_liquid_plates/get_raw_data_file?" + 'plate=' + selected_plate;
}




function createPlateChoice(plateMap)
{
	$td_plate_choice = $('<td>', {
		
		id: "td_plate_choice",
		class: "td_reg_flow"
	});
	
	$tr_flow1.append($td_plate_choice);	
	
	createCurrentControl($td_plate_choice, plateMap, plateChange);
}



function plateChange(plateMap)
{
	//console.log('plateChange');
	
//	console.log('plateMap.focused_plate: ', plateMap.focused_plate);
	
	updatePlateGUI(plateMap);
	
	updateCellChooser(plateMap);
	updateFocusedExperiment(plateMap);
	//updatePlateChoosingGUI(plateMap);
	
}

function updateFocusedExperiment(plateMap)
{
	
}



function updateCellChooserGUI(platePattern)
{
	$div_cell_chooser.empty();
	
	//console.log('updateCellChooserGUI: ');
	
	createCellChooser(platePattern, $div_cell_chooser); 
	
	var plate_key = platePattern.createPlateKey();
	//console.log('plate_key: ', plate_key);
	
	if(plate_key == undefined)
	{
		
	}
	else
	{
		//console.log('JSON.stringify(cell_state): ', JSON.stringify(cell_state));
		
		for(var cell_id in platePattern.saved_cells[plate_key])
		{
			$('#'+cell_id).toggleClass('unchecked_cell checked_cell');
		}
	}
}




