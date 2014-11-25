

var csrftoken;

var go_again;

var t_snap_debug;

var MAIN_CONTEXT = 'main';
var COMPARED_CONTEXT = 'compared';


var plateMap2;



$(document).ready(function()
{
	csrftoken = getCookie('csrftoken');
	//console.log("csrftoken: ", csrftoken);
	
	var plateMap = new PlateMap(MAIN_CONTEXT);
	var dataMap = new CopySnapshotMap(plateMap.context_view);
	plateMap.setDataMap(dataMap);

	plateMap2 = new PlateMap(COMPARED_CONTEXT);
	var dataMap2 = new CopySnapshotMap(plateMap2.context_view);
	plateMap2.setDataMap(dataMap2);
	
	
	createActionBarGUI();
	createSnapshot(plateMap);
	createComparisonGUI($(':eq(0)'), plateMap, plateChange);
	createSnapshotGUI(plateMap, $td_current_control, scoodBatch);
	
	
	plateMap.getMap([ALL_NICKNAMES], false, updatePlateChoosingGUI);
	
		
	
	go_again = false;
	
	$(".batch_gui").hide();
	$('.snapshot_gui').hide();
	
	
	createCurrentAnalysis(plateMap);
	
	// $("body").keypress(function(e){
        // // alert(e.which);
        // snapshot();
//         
    // });
    
    libraryFilter = new LibraryFilter(plateMap);
    
    $div_choose = $('<div>', {
		id:"div_choose"
	});
	
	$('body').append($div_choose);
    
    $div_reg = $('<div>', {
		id:"div_reg"
	});
	
	$('body').append($div_reg);
	
	$div_reg.hide();
	$div_choose.hide();
    
    
    $t_forms = $('<table>', {
		id: "t_forms"
	});	
	
	$div_reg.append($t_forms);
	
	$t_choice = $('<table>', {
		id: "t_choice"
	});
	
	$div_choose.append($t_choice);
	
		$tr_flow1 = $('<tr>', {
			id : "tr_flow1"
		});

		$t_choice.append($tr_flow1);
	
	
		$tr_reg_flow = $('<tr>', {
			id : "tr_reg_flow"
		});

		$t_forms.append($tr_reg_flow);
    
    
    createLibCopyRegGUI($tr_reg_flow, plateMap);
    
    
    libraryFilter.getMap($s_users);
    
	populateLibCopyGUI(plateMap, libraryFilter, $tr_flow1, $div_lib_form, $s_users);
	
	
    
});


function createComparisonGUI(parent_element, plateMap, update)
{
	//console.log('createComparisonGUI');
	
	$t_frame = $('<table id="t_frame"></table>');
	
		$tr_frame = $('<tr id="tr_frame"></tr>');
	
			$td_comparison = $('<td id = "td_comparison"></td>');
			$td_compared_images = $('<td id = "td_compared_images"></td>');
	
	createCurrent($td_comparison, plateMap, update);
	createCompared($td_compared_images, plateMap2);

	
	$tr_frame.append($td_comparison);
	$tr_frame.append($td_compared_images);
	
	$t_frame.append($tr_frame);
	
	parent_element.append($t_frame);
	
	$t_analysis_frame = $('<div id=t_analysis_frame></div>');
	
	parent_element.append($t_analysis_frame);
}



function createCompared(parent_element, plateMap)
{
	$t_compared = $('<table id="t_compared"></table>');
	
		$td_compared_img = $('<td id = "td_compared_img", class="td_reg_flow"></td>');
	
			$img_compared = $('<img id="img_compared", src="/static/yeast_libraries/img/384_0002.jpg" width="600", height="400"></img>');
			$td_compared_img.append($img_compared);

            $b_show_unprocessed_compared = $('<input>', {
					type: "button",
					id : "$b_show_unprocessed_compared",
                    class: "b_processed",
					value: "View Processed",
					click: function()
					{
						if(this.value == "View Processed")
						{
							showImage(plateMap2.dataMap, true);
							this.value = "View Unprocessed";
						}
						else
						{
							showImage(plateMap2.dataMap, false);
							this.value = "View Processed";
						}

					}
				}
			);

            $td_compared_img.append('<br>');
			$td_compared_img.append($b_show_unprocessed_compared);



		
		$t_compared.append($td_compared_img);
	
	
		$td_compared_control = $('<td id="td_compared_control", class="td_reg_flow"></td>');
			$td_compared_control.append('<h1 class="control_header">Compared Plate</h1>');
			
			$td_compared_control.append('<h2 class="control_label">Library (Type)</h2>');
			$td_compared_control.append('<select id="compared_library_list", class="control_select" multiple>');
			
			$td_compared_control.append('<h2 class="control_label"           >Stack (copy)</h2>');
			$td_compared_control.append('<select id="compared_stack_list" multiple></select>');	
			

				$div_compared_control = $('<div id="div_compared_control"></div>');
				
				
					$compared_plate_counter = $('<h2 class="control_label">NOO Plates</h2>');
					
					$div_compared_control.append($compared_plate_counter);
				
			
					$compared_browser = $('<div id="compared_browser"></div>');
					
						$img_compared_back = $('<img>',{
							id : "compared_back",
							src : "/static/yeast_libraries/img/back.png",
						    text: 'Back',
						    title: 'Back',
						    href: '#',
						    click: function(){plateMap.backPlate(plateChange);}
						});
						
						$compared_browser.append($img_compared_back);
						
						
						$img_compared_next = $('<img>',{
							id : "compared_next",
							src : "/static/yeast_libraries/img/next.png",
						    text: 'Next',
						    title: 'Next',
						    href: '#',
						    click: function(){ plateMap.nextPlate(plateChange);}
						});
					
					$compared_browser.append($img_compared_next);
				
				$div_compared_control.append($compared_browser);
				
					$compared_batch_counter = $('<h2 id="batch_label_compared", class="batch_gui",>No Batches</h2>');
					
					$div_compared_control.append($compared_batch_counter);
					
					$compared_batch_browser = $('<div id="compared_batch_browser"></div>');
					
						$img_compared_batch_back = $('<img>',{
							id : "compared_batch_back",
							class : "batch_gui",
							src : "/static/yeast_libraries/img/back.png",
						    text: 'Back',
						    title: 'Back',
						    href: '#',
						    click: function(){ scoodBatch(plateMap.dataMap, false);}
						});
						
						$compared_batch_browser.append($img_compared_batch_back);
						
						
						$img_compared_batch_next = $('<img>',{
							id : "compared_batch_next",
							class : "batch_gui",
							src : "/static/yeast_libraries/img/next.png",
						    text: 'Next',
						    title: 'Next',
						    href: '#',
						    click: function(){ scoodBatch(plateMap.dataMap, true);}
						});
					
					$compared_batch_browser.append($img_compared_batch_next);
				
				$div_compared_control.append($compared_batch_browser);
		
		
			$td_compared_control.append($div_compared_control);
			
		$t_compared.append($td_compared_control);
	
	parent_element.append($t_compared);	
}



function updatePlateChoosingGUI(plateMap)
{
	var context = plateMap.context_view;
	console.log('updatePlateChoosingGUI with', context, 'context');
	
	if(context == MAIN_CONTEXT)
	{
		populatePlateChooser(plateMap, plateChange, $('#library_list'), $('#stack_list'), promptCopyRegister);
		
		//if(plateMap2.map == undefined)
		//{
			//console.log('initializing compared');
		
			plateMap2.map = plateMap.map;
			plateMap2.initiate();
			updatePlateChoosingGUI(plateMap2);
		//}
			var nicknames = $s_users.val();
			
			if(!nicknames)
			{
				nicknames = ALL_NICKNAMES;
			}
			
			copyRegister.getAndDisplayDataFromServer(nicknames);
		
	}
	else if(context == COMPARED_CONTEXT)
	{
		populatePlateChooser(plateMap, plateChange, $('#compared_library_list'), $('#compared_stack_list'), promptCopyRegister);
	}
}


function plateChange(plateMap)
{
	//console.log('plateChange');
	
	//console.log('plateMap.focused_plate: ', plateMap.focused_plate);
	
	updatePlateGUI(plateMap);
	updateSnapshotMap(plateMap);
}





function updateSnapshotMap(plateMap)
{
	//console.log('updateSnapshotMap');
	
	var dataMap = plateMap.dataMap;
	
	if(plateMap.focused_stack_name === undefined)
	{
		console.log('plateMap.focused_stack_name === undefined');
		//promptCopyRegister();
	}
	else
	{
		var copy_pk = plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['pk'];
		//console.log('copy_pk:', copy_pk);
		
		
		if(dataMap.copy_pk === undefined || dataMap.copy_pk != copy_pk)
		{
			//console.log('initiating dataMap');
			
			
			dataMap.copy_pk = copy_pk;
			dataMap.getMap(updateBatchGUI);
			
			if(plateMap2.dataMap.copy_pk == copy_pk)
			{
				//console.log('updating compared');
				
				plateMap2.dataMap.getMap(updateBatchGUI);
			}
		}
		else
		{
			//console.log('using old dataMap');
			
			if(dataMap.map === undefined)
			{
				//console.log('dataMap.map === undefined');
			}
			else
			{
				dataMap.focused_plate = plateMap.focused_plate;
			}
			
			updateBatchGUI(plateMap.dataMap);
		}	
	}
}


function updateBatchGUI(dataMap)
{
	//console.log('updateBatchGUI');
	
	var batch_counter = $current_batch_counter;
	
	if(dataMap.context_view == COMPARED_CONTEXT)
	{
		batch_counter = $compared_batch_counter;
	}
	
	
	var snapshotMap = dataMap.getFocusedSnapshotMap();
	
	var batch_for_user = 'No Snapshots';
	
	//console.log(snapshotMap);
	
	if(snapshotMap === undefined || snapshotMap.focused_batch === undefined)
	{
		//console.log('no focused batch');
		
		batch_for_user = 'No Batches';
	}
	else
	{
		batch_for_user = 'Batch # ' + (snapshotMap.focused_batch + 1) + ' of ' + (snapshotMap.total_batches);	
	}
	
	batch_counter.html(batch_for_user);
	
	var processed = true;
	
	if(dataMap.context_view == COMPARED_CONTEXT)
	{
		processed = false;
	}
	
	showImage(dataMap, processed);
}


function promptCopyRegister(plateMap)
{
	if(plateMap.context_view == MAIN_CONTEXT && confirm(plateMap.focused_lib_name + ' Library/Plate Has no registered copies!\nDo Yo want to register a copy?'))
	{
		console.log('harpoozel flunch');
		
		$('#img_register').click();
	}
}



function analyzeSnapshot(plateMap)
{
	//$('#browser').empty();
	console.log('analyzeSnapshot()');
	
	try
	{
		var lib_pk = plateMap.map[plateMap.focused_lib_name]['pk'];
		console.log('lib_pk: ', lib_pk);
		
		var psm = plateMap.dataMap.getFocusedSnapshotMap();
		
		var snapshot_pk = psm.map['batches'][psm.focused_batch]['snapshots'][psm.focused_snapshot]['pk'];
		console.log('snapshot_pk: ', snapshot_pk);
	}
	catch(err)
	{
		console.log(err);
		alert('No snapshot to analyze');
		return;
	}
	
	
	
	var j = ''.concat('lib_pk=', lib_pk, '&snapshot_pk=', snapshot_pk,'&get_excel=', 'false');
	
	console.log('request:     ', j);
	$.get( "/yeast_libraries/getSnapshotAnalysis", j, function(data) 
		{
			// console.log('data:');
			// console.log(data);
		  
		  	showAnalysis(JSON.parse(data), 'analyze', j, plateMap, true, true);
		}
	);

	//open(''.concat(BASE_URL, '/yeast_libraries/compare_snapshots?', j), 'copy session', "height=800, width=800, top=200, left=400");
}

function analyzeSnapshotBatch(plateMap, discrepancy_report)
{
	//$('#browser').empty();
	console.log('analyzeSnapshotBatch()');
	
	try
	{
		var copy_pk = plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['pk'];
		console.log('copy_pk: ', copy_pk);
		
		var batch_index = plateMap.dataMap.getFocusedSnapshotMap().focused_batch;
	}
	catch(err)
	{
		console.log(err);
		alert('No batch to analyze');
		return;
	}
	
	var j = ''.concat('copy_pk=', copy_pk, '&batch_index=', batch_index, '&get_excel=', 'true', '&discrepancy_report=', discrepancy_report);
	
	// console.log('request:     ', j);
	
	location.href="/yeast_libraries/getBatchSnapshotAnalysis?" + j;

}


function analyzeSnapshotOverLib(lib_only, plateMap, discrepancy_report)
{
	console.log('analyzeSnapshotOverLib()');
	console.log('lib_only: ', lib_only);

	try
	{
		var lib_pk = plateMap.map[plateMap.focused_lib_name]['pk'];
		console.log('lib_pk: ', lib_pk);
		
		var psm = plateMap.dataMap.getFocusedSnapshotMap();
		var plate_pk = psm.plate_pk;
		console.log('plate_pk: ', plate_pk);
		
		if(lib_only)
		{
			var snapshot_pk = 1;
		}
		else
		{
			var snapshot_pk = psm.map['batches'][psm.focused_batch]['snapshots'][psm.focused_snapshot]['pk'];
			console.log('snapshot_pk: ', snapshot_pk);
			//analysis_exists = ; 
		}
	}
	catch(err)
	{
		console.log(err);
		alert('No snapshot to analyze');
		return;
	}
	
	var j = ''.concat('lib_pk=',lib_pk,'&snapshot_pk=', snapshot_pk,'&plate_pk=', plate_pk, '&get_excel=', 'false', '&discrepancy=', discrepancy_report);
	
	//console.log('batch_operation: ', batch_operation);
	
	
	// console.log('request:     ', j);	
	$.get( "/yeast_libraries/getSnapshotOverLibAnalysis", j, function(data) 
		{
			// console.log(lib_only);
			// console.log('data:');
			// console.log(data);
		  	
		  	if(lib_only)
		  	{
		  		showAnalysis(JSON.parse(data), 'lib_pattern', j, plateMap, true, true);
		  	}
		  	else
		  	{
		  		showAnalysis(JSON.parse(data), 'analyze_over_lib', j, plateMap, true, true);
		  	}
		  		
		}
	);

	//open(''.concat(BASE_URL, '/yeast_libraries/compare_snapshots?', j), 'copy session', "height=800, width=800, top=200, left=400");
}



function compareSnapshots(plateMap)
{
	if(plateMap.focused_stack_name === undefined || plateMap2.focused_stack_name === undefined)
	{
		alert('To compare youe must choose plates on both sides');
		clearAnalysis();
		return;
	}
	
	
	
	try
	{	
		var psm = plateMap.dataMap.getFocusedSnapshotMap();
		var psm2 = plateMap2.dataMap.getFocusedSnapshotMap();		
		
		var plate_pk = psm.plate_pk;
		console.log('plate_pk: ', plate_pk);
		
		var plate_pk2 = psm2.plate_pk;
		console.log('plate_pk2: ', plate_pk2);
		
		var snapshot_pk = psm.map['batches'][psm.focused_batch]['snapshots'][psm.focused_snapshot]['pk'];
		console.log('snapshot_pk: ', snapshot_pk);
		
		var snapshot_pk2 = psm2.map['batches'][psm2.focused_batch]['snapshots'][psm2.focused_snapshot]['pk'];
		console.log('snapshot_pk2: ', snapshot_pk2);
	}
	catch(err)
	{
		console.log(err);
		alert('No snapshot to analyze');
		return;
	}
	
	var j = ''.concat('plate_pk=', plate_pk, '&snapshot_pk=', snapshot_pk, '&compared_plate_pk=', plate_pk2, '&compared_snapshot_pk=', snapshot_pk2, '&get_excel=', 'false');
	
	// console.log('request:     ', j);	
	$.get( "/yeast_libraries/compare_snapshots", j, function(data) 
		{
		  // console.log('data:');
		  // console.log(data);
		  
		  showAnalysis(JSON.parse(data), 'compare', j, plateMap, true, true);
		}
	);
	
	//open(''.concat(BASE_URL, '/yeast_libraries/compare_snapshots?', j), 'copy session', "height=800, width=800, top=200, left=400");
}


function compareCopyBatches(plateMap)
{
	if(plateMap.focused_stack_name === undefined || plateMap2.focused_stack_name === undefined)
	{
		alert('To compare youe must choose plates on both sides');
		clearAnalysis();
		return;
	}

	try
	{	
		var copy_pk = plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['pk'];
		console.log('copy_pk: ', copy_pk);
		
		var batch_index = plateMap.dataMap.getFocusedSnapshotMap().focused_batch;
		
		var copy_pk2 = plateMap2.map[plateMap2.focused_lib_name]['stacks'][plateMap2.focused_stack_name]['pk'];
		console.log('copy_pk2: ', copy_pk2);
		
		var batch2_index = plateMap2.dataMap.getFocusedSnapshotMap().focused_batch;
	}
	catch(err)
	{
		console.log(err);
		alert('No snapshot to analyze');

		return;
	}
	
	
	if(copy_pk == copy_pk2 && batch_index == batch2_index)
	{
		console.log('pointless to compare a picture batch to itself');
		alert('pointless to compare a picture batch to itself');
		return;
	}
	
	
	var j = ''.concat('copy_pk=', copy_pk, '&batch_index=', batch_index, '&copy_pk2=', copy_pk2, '&batch2_index=', batch2_index, '&get_excel=', 'true');
	
	// console.log('request:     ', j);	
	location.href="/yeast_libraries/compare_copies?" + j;
}



function createSnapshot(plateMap)
{
	$img_snapshot = $('<img>',{
		id : "snapshot",
		src : "/static/yeast_libraries/img/snapshot.png",
	    text: 'This is blah',
	    title: 'Blah',
	    href: '#',
	    click: function(){ snapshot(plateMap);}
	});
	
	$('#div_snapshot').append($img_snapshot);
	
		
	$b_new_batch = $('<input>', {
		id : "b_new_batch",
		class : "batch_gui",
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
	
	
	$('#div_snapshot').append($b_new_batch);
	
	
	$img_last_snapshot = $('<img>',{
		id : "img_last_snapshot",
		src : "/static/yeast_libraries/img/empty.png",
		width: "300",
		height: "200"
	});
	
	//$img_last_snapshot.load(function() { console.log('         received image!!!!!!'); });
	
	$('#div_snapshot').append($img_last_snapshot);
	
	
	$div_batch = $('<div id="div_batch"></div>');
}


function createActionBarGUI()
{
	// $t_wrap_reg_lib = $('<table>', {
		// id: t_wrap_reg_lib,
	// });
// 	
		// $tr_wrap_reg_lib1 = $('<tr>', {
			// id: tr_wrap_reg_lib1,
		// });
	$t_control = $('<table>', {
		id: 't_control'
	});
	
	$('#div_choice_action').append($t_control);
	
		$tr_control1 = $('<tr>',{
			id: 'tr_control1'
		});
	
		$t_control.append($tr_control1);	
	
			$td_reg_copy = $('<td>', {
				id: "td_reg_copy"
			});
			
			$tr_control1.append($td_reg_copy);
		
				$('<img>',{
					id : "img_register",
					src : "/static/yeast_libraries/img/bread_sliced.png",
				    text: 'This is blah',
				    title: 'Register Lib or Copy',
				    href: '/yeast_libraries/stack_register_gui/',
				    click: function(){ $div_reg.toggle();}
				}).appendTo($td_reg_copy);
				
				$td_reg_copy.append('<h2 class="control_clickable">Register Lib or Copy</h2>');
		
			$td_toggle_batch_gui = $('<td>', {
				id: "td_toggle_batch_gui"
			});
				
			$tr_control1.append($td_toggle_batch_gui);
	
				$('<img>',{
					id : "img_show_batches",
					src : "/static/yeast_libraries/img/stack_bread.png",
				    text: 'This is blah',
				    title: 'Show Batches',  
				    href: '#',
				    click: function(){ $(".batch_gui").toggle();}
				}).appendTo('#td_toggle_batch_gui');
		
				$td_toggle_batch_gui.append('<h2 class="control_clickable">Show Batches</h2>');
	
	
			$td_toggle_cam = $('<td>', {
				id: "td_toggle_cam"
			});
				
			$tr_control1.append($td_toggle_cam);
	
				$img_snapshot_gui = $('<img>',{
					id : "img_snapshot_gui",
					src : "/static/yeast_libraries/img/shutter.png",
				    text: 'This is blah',
				    title: 'Snapshots',
				    href: '#',
				    click: function(){ $('.snapshot_gui').toggle();}
				});
				
				$img_snapshot_gui.draggable();
		
				$td_toggle_cam.append($img_snapshot_gui);
				$td_toggle_cam.append('<h2 class="control_clickable">Show Cam</h2>');
	
	//$('#to_create_lib').hide();
	
	
	$header = $('<f id="header">Image Analysis</f>');
	
	$('#div_choice_action').append($header);
}



function showImage(dataMap, is_processed)
{
	var img = $img_current;
	var selector = 'processed_image_path';
	

	if(dataMap.context_view == COMPARED_CONTEXT)
	{
		img = $img_compared;
	}
	
	if(! is_processed)
	{
		selector = 'image_path';
	}
	
	// console.log('');
	// console.log('dataMap.total_plates: ', dataMap.total_plates);
	// console.log('dataMap.focused_plate: ', dataMap.focused_plate);
	// console.log('');
// 	
	var psm = dataMap.getFocusedSnapshotMap();
	
	var img_path = "/static/yeast_libraries/img/empty.png";

	// console.log('psm.focused_batch: ', psm.focused_batch);
	// console.log('psm.focused_snapshot: ', psm.focused_snapshot);
	// console.log('psm.plate_pk: ', psm.plate_pk);


	if(!(psm === undefined || psm.focused_snapshot === undefined))
	{
		try
		{
			img_path = psm.map['batches'][psm.focused_batch]['snapshots'][psm.focused_snapshot][selector].toString();
			
			if(img_path == '' && selector == 'processed_image_path')
			{
				selector = 'image_path';
				img_path = psm.map['batches'][psm.focused_batch]['snapshots'][psm.focused_snapshot][selector].toString();
			}
		}
		catch(err)
		{
			console.log('error:', err);
			
			img_path = "/static/yeast_libraries/img/empty.png";
		}
		
		//console.log('img_path: ', img_path);
		
		if(! (endsWith(img_path,'.jpg') || endsWith(img_path,'.jpeg')))
		{
            if(img_path = 'failed_to_analyze')
            {
                img_path = "/static/yeast_libraries/img/failed_analysis.png";
            }
            else
            {
                img_path = "/static/yeast_libraries/img/empty.png";
            }

		}	
	}
	
	putImageIn(img_path, img);
}



function snapshot(plateMap)
{
	var dataMap = plateMap.dataMap;
	
	if(typeof plateMap.focused_stack_name === 'undefined')
	{
		alert('Please choose a library and a copy in the scroll bars on the lower left');
 	}
 	else
 	{ 		
 		if(plateMap.focused_plate == 1)
 		{
 			if(go_again)
 			{
 				// if(!confirm('It appears you have completed the stack\n do you wish to continue?'))
	 			// {
	 				// go_again = false;
	 				// return;
	 			// }
 			}
 			else
 			{
 				go_again = true;
 			}
 		}
 		
 		//console.log('trying to find snapshot');
		
		var batch_num = plateMap.current_plate_batch;
		
		if(batch_num === undefined)
		{
			batch_num = 1;
		}
		
		if($b_new_batch.val().indexOf("New") != -1)
		{
			batch_num = plateMap.total_current_plate_batches + 1;
			$b_new_batch.prop('value', "Same Batch");
		}
		
		
		var stack_pk = plateMap.map[plateMap.focused_lib_name]['stacks'][plateMap.focused_stack_name]['pk'];
		
		//console.log('stack_pk:', stack_pk);
		
	
		var j  = ''.concat('library=', plateMap.focused_lib_name, '&', 'stack=', plateMap.focused_stack_name, '&', 'stack_pk=', stack_pk, '&','plate_num=', (plateMap.focused_plate + 1), '&', 'batch_num=', batch_num);
	
		console.log('snapshot query');
		console.log(j);
		
		var t1 = new Date().getTime();
		

		
		$.get( "/yeast_libraries/snapshot", j, function(data) 
		{
			  console.log('snapshot callback:');
			  console.log(data);
			  
			  if(data=='cam_error')
			  {
			  	alert('Camera failed to take a picture');
			  	return;
			  }
			  
			  var j_image_dict = JSON.parse(data);
			  
			  var snapshot_pk = j_image_dict['snapshot_pk'];
			  var image_path = j_image_dict['image_path'];
			  	
		  	  console.log('snapshot callback:  imge_path: ', image_path);	
		  	  $img_last_snapshot.attr('src', '/yeast_libraries/get_image/?image_full_path=' + image_path + "&stam=" + Math.random());
		  	  

			  var t2 = new Date().getTime();
			  t = t2-t1;
			  console.log('Time for receiving picture: ', t);
			  
			  var library = j_image_dict['library'];
			  var stack = j_image_dict['stack'];
			  var plate_num = j_image_dict['plate_num'];
			  var batch_num = j_image_dict['batch_num'];
			  
			  if(plateMap.focused_stack_name == stack)
			  {
			 		var plateSnapshotMap = dataMap.getSnapshotMap(plate_num);
			 		plateSnapshotMap.getMap(function()
			 		{
			 			updateComparedSnapshotMap(dataMap, plateSnapshotMap, plate_num);
			 			updateBatchGUI(dataMap);
			 		});
			  }
			  
			  
			  var j_batches = plateMap.map[library]['stacks'][stack]['plates'][plate_num - 1];
			  
			  plateMap.nextPlate(plateChange);
			  // console.log('');
			  // console.log('');
			  // console.log('JSON.stringify(plateMap.map):');
			  // console.log(JSON.stringify(plateMap.map));
			  
			  var request_params  = ''.concat('snapshot_pk=', snapshot_pk, '&process_pk=', j_image_dict['process_pk']);
			  
			  // console.log('request_params', request_params);
			
			var t_snap_debug = new Date().getTime();
			
			console.log('start folowup time', t_snap_debug);
			
			snapshotFollowup(dataMap, request_params);
		});
 	}
}


function snapshotFollowup(dataMap, request_params)
{
	console.log('snapshotFollowup...');
	// console.log('request_params', request_params);
// 	
	// console.log('before timeout', new Date().getTime());
	
	$.ajax
	(
		{ 
			url: "/yeast_libraries/snapshot_follow_up", 
			data: request_params,
			success: function(response)
			{
				var j_dict = JSON.parse(response);
				console.log('j_dict: ', j_dict);
				
				var snapshot_pk = j_dict['snapshot_pk'];
				var process_pk = j_dict['process_pk'];
				var status = j_dict['status'];
				
				var request_params  = ''.concat('snapshot_pk=', snapshot_pk, '&process_pk=', process_pk);
				
				
				console.log('time after timeout', new Date().getTime());
				console.log('request_params: ', request_params);
				
				if(status == "bussy")
				{
					checkSnapshotStatus(dataMap, request_params);
				}
				else
				{
					console.log('total folowup time', new Date().getTime() - t_snap_debug);
					console.log('Yoffi Nechama');
					var processed_image_path = j_dict['processed_image_path'];
					console.log('processed_image_path: ', processed_image_path);
					
					var plate_index = j_dict['plate_index'];
					
					var psm = dataMap.getSnapshotMap(plate_index);
					psm.getMap(function()
					{
						console.log('spadinkee');
						updateComparedSnapshotMap(dataMap, psm, plate_index);
						updateBatchGUI(dataMap);
					});
				}
			}
		}
	);
}


function updateComparedSnapshotMap(dataMap, plateSnapshotMap, plate_num)
{
	console.log('');
	console.log('got re back');
	
	if(dataMap.copy_pk == plateMap2.dataMap.copy_pk)
	{
		console.log('same copy');
		console.log('plate_num: ', plate_num);
		
		var plateSnapshotMap2 = plateMap2.dataMap.getSnapshotMap(plate_num);
		plateSnapshotMap2.initiate(plateSnapshotMap.map);
		updateBatchGUI(plateMap2.dataMap);
	}
	else
	{
		console.log('different copy');
	}
	
	console.log('');
}




var timeoutId;

function checkSnapshotStatus(dataMap, request_params)
{
	console.log('dealWithSnapshotFollowup...');
	console.log('request_params: ', request_params);
	//clearTimeout(timeoutId);
	
	//timeoutId = setTimeout
	console.log('settimeout', setTimeout
	(	
		function(){snapshotFollowup(dataMap, request_params);},
		10000
	));
	
		  // $.each(document.cookie.split(/; */), function()  {
	  // var splitCookie = this.split('=');
	  // console.log('key: ', splitCookie[0], '  value is: ', splitCookie[1]);
	// });
}




function getCookie(name) 
{
	  var regexp = new RegExp("(?:^" + name + "|;\s*"+ name + ")=(.*?)(?:;|$)", "g");
	  var result = regexp.exec(document.cookie);
	  return (result === null) ? null : result[1];
}



function createCurrentAnalysis(plateMap)
{
	$div_current_analysis = $('<div id="div_current_analysis"></div>'); 

        $div_current_analysis_control = $('<div id="div_current_analysis_control"></div>');
		$div_current_analysis_control1 = $('<div id="div_current_analysis_control1"></div>');
        $div_current_analysis_control2 = $('<div id="div_current_analysis_control2"></div>');


            $b_analyze_entire_batch = $('<input>', {
					type: "button",
					id : "$b_analyze_entire_batch",
                    class: "b_analysis_csv",
					value: "Copy Plates Analyses",
					click: function()
					{
                        $toast.toast('this might take some time...2 mins probably, a fix is due', 5000);

						console.log('this.id: ', this.id);
						analyzeSnapshotBatch(plateMap);
					}
				}
			);


			$div_current_analysis_control2.append($b_analyze_entire_batch);



			$b_lib_discrepancy_report = $('<input>', {
					type: "button",
					id : "b_lib_discrepancy_report",
                    class: "b_analysis_csv",
					value: 'Library-Copy Discrepancy Report',
					click: function(){ analyzeSnapshotBatch(plateMap, true);}
				}
			);
		
			$div_current_analysis_control2.append($b_lib_discrepancy_report);


            $b_snapshot_discrepancy_history_report = $('<input>', {
					type: "button",
					id : "b_snapshot_discrepancy_history_report",
                    class: "b_analysis_csv",
					value: 'Snapshot Discrepancy History Report',
					click: function(){

                        $toast.toast('This might take long depending how many ancestors the copy has')

                        try
                        {
                            var sm = plateMap.dataMap.getFocusedSnapshotMap(plateMap.focused_plate);

                            var batch_index = sm.focused_batch;
//                            console.log('batch_index: ', batch_index);
//                            console.log(sm)
                            var snapshot_pk = sm.map['batches'][batch_index]['snapshots'][0]['pk'];
                            console.log(snapshot_pk);
                        }
                        catch(err)
                        {
                            console.log(err);
                            alert('No snapshot to analyze');
                            return;
                        }

                        var j = ''.concat('snapshot_pk=', snapshot_pk, '&batch_index=', batch_index, '&get_excel=', 'true');

                        // console.log('request:     ', j);

                        location.href="/yeast_libraries/getSnapshotAnalysisHistory?" + j;
                     }
				}
			);

			$div_current_analysis_control2.append($b_snapshot_discrepancy_history_report);


            $b_library_csv = $('<input>', {
					type: "button",
					id : "b_library_csv",
                    class: "b_analysis_csv",
					value: 'Library CSV',
					click: function(){

                        $toast.toast('This might take a couple minutes according to library size [fix in next version]')

                        var library_pk = plateMap.getFocusedLibraryID();

                        //console.log('library_pk:', library_pk, '   text:', $("#select_library option:selected").text());

                        var j = ''.concat('library_pk=', library_pk, '&get_excel=', 'true');

                        console.log('request:     ', j);

//                        console.log('plateMap.focused_lib_name: ', plateMap.focused_lib_name)

                        location.href="/yeast_libraries/library_info?" + j;
                     }
				}
			);

			$div_current_analysis_control2.append($b_library_csv);

		
			$b_analyze_over_lib_current = $('<input>', {
					type: "button",
					id : "b_analyze_over_lib_current",
                    class: "b_show_analysis",
					value: "Analyze Over Library",
					click: function(){ analyzeSnapshotOverLib(false, plateMap);}
				}
			);
		
			$div_current_analysis_control1.append($b_analyze_over_lib_current);
					
			$b_analyze_current = $('<input>', {
					type: "button",
					id : "b_analyze_current",
                    class: "b_show_analysis",
					value: "Analyze",
					click: function(){ analyzeSnapshot(plateMap);}
				}
			);
		
			$div_current_analysis_control1.append($b_analyze_current);
			
			$b_lib_pattern = $('<input>', {
					type: "button",
					id : "b_lib_pattern",
                    class: "b_show_analysis",
					value: "Library Pattern",
					click: function(){ analyzeSnapshotOverLib(true, plateMap);}
				}
			);
		
			$div_current_analysis_control1.append($b_lib_pattern);
		
			$b_compare = $('<input>', {
					type: "button",
					id : "$b_compare",
                    class: "b_show_analysis",
					value: "Compare",
					click: function(){ compareSnapshots(plateMap);}
				}
			);
		
			$div_current_analysis_control.append($b_compare);
			
			
			$b_compare_batches = $('<input>', {
					type: "button",
					id : "$b_compare_batches",
                    class: "b_analysis_csv",
					value: "Compare Copies",
					click: function()
					{
                        $toast.toast('comparing...', 3000);
						console.log('this.id: ', this.id);
						compareCopyBatches(plateMap);
					}
				}
			);
		
			$div_current_analysis_control.append($b_compare_batches);
			
			
		
		$div_current_analysis.append($div_current_analysis_control);
        $div_current_analysis.append($div_current_analysis_control1);
        $div_current_analysis.append($div_current_analysis_control2);

		
	$t_analysis_frame.append($div_current_analysis);
	
	
	$toast = $('<div class="toast">Comparing...</div>');

    $toast.toast = function(text, time)
    {
        if(time == undefined)
        {
            time = 3000;
        }

        this[0].innerHTML = text;
        this.show();
        console.log(this, text);
        setTimeout(function(){$toast.hide()}, time);
    }

	$div_current_analysis_control.append($toast);
	
	$toast.hide();
}



function showAnalysis(data, type, get_query, plateMap, clear, open_window)
{
	var width = data.length;
	var height = data[0].length;
	//console.log('width ', width, 'height: ', height);	
	
	if(clear)
	{
		clearAnalysis();
	}
		
	var tr = $('<tr></tr>');
	
	for(var j=0; j<=height; j++)
	{	
		if (j == 0)
		{
			var t = '';
		}
		else if(j<10)
		{
			t = '0'+j;
		}
		else
		{
			t = j;
		}
		
		
		var td = $('<td></td>', {
			text: t,
			class: "analysis_row"
			
		});
	
		tr.append(td); 
	}
	
	$t_current_analysis.append(tr);
	
	for(var i=0; i<width; i++)
	{
		letter = String.fromCharCode(97 + i).toUpperCase();
		
		tr = $('<tr></tr>');
		
		td = $('<td class="analysis_row">'+ letter +'</td>');
		
		tr.append(td); 

		
		for(j=1; j<=height; j++)
		{
			var class_name = 'analysis_row';
			
			var pic_locus = data[i][j-1];
			
			if(type=='analyze_over_lib')
			{
				pic_locus = data[i][j-1][1];
				lib_locus = data[i][j-1][0];
				
				//console.log('library cell value:', lib_locus, '   analysis value: ', pic_locus);
				
				if(pic_locus==0)
				{
					pic_locus = '';
					
					if(lib_locus==0)
					{
						class_name = 'analysis_td_true_negative';	
					}
					else
					{
						class_name = 'analysis_td_false_negative';
						pic_locus = '*';
					}
				}
				else
				{
					pic_locus = 'O';
					
					if(lib_locus==0)
					{
						class_name = 'analysis_td_false_positive';	
					}
					else
					{
						class_name = 'analysis_td_true_positive';
					}
				}		
			}
			else if(type=='lib_pattern')
			{
				lib_locus = data[i][j-1][0];
				pic_locus = '';
				
				//console.log('library cell value:', lib_locus);
				
				if(lib_locus==0)
				{
					class_name = 'analysis_td_true_negative';
				}
				else
				{
					class_name = 'analysis_td_true_positive';
				}	
			}
			else if(type=='analyze')
			{
				if(pic_locus==0)
				{
					pic_locus = '';
					class_name = 'analysis_td_true_negative';
				}
				else
				{
					pic_locus = '';
					class_name = 'analysis_td_true_positive';
				}				
			}
			else if(type=='compare')
			{
				if(pic_locus==0)
				{
					pic_locus = 'V';
				}
				else if(x==1)
				{
					pic_locus = 'X';
				}
				else
				{
					pic_locus = '?';
				}				
			}
			
			//console.log('class_name: ', class_name);
			
			td = $('<td></td>', {
				text: pic_locus,
				class: class_name
			});	
			tr.append(td); 
		}
		
		$t_current_analysis.append(tr);
	}
	
	$div_current_analysis.append($t_current_analysis);
	
	analysis_html = $t_current_analysis[0].outerHTML;
	//console.log(analysis_html);
		
	// var x = window.open();
	// x.document.write('kloom');
	// console.log('grandma???');
	
	
	// var analysis_window = window.open("","analysis_window","width=1000,height=1000");
	// analysis_window.document.write("<p>This is 'analysis_window'</p>");
// 	
	// analysis_window.document.write($t_current_analysis[0].outerHTML);
	if(open_window)
	{
		var x = open('/yeast_libraries/show_analysis',"_blank","width=1200,height=1050");
		x.location.reload();
		console.log('reloaded??##@@@?');
		
		//x.analysis_html = analysis_html;
		x.data = data;
		x.type = type;
		x.stack = plateMap.focused_stack_name;
		x.plate = plateMap.focused_plate;
		x.batch = plateMap.dataMap.getFocusedSnapshotMap().focused_batch;

        console.log('x.batch: ', x.batch);


		if(get_query != undefined)
		{
			x.get_query = get_query.replace('false', 'true');
		}
	}
}



function clearAnalysis()
{	
	if($b_show_unprocessed.val() == "View Processed")
	{
		$b_show_unprocessed.click();
	}
	
	try
	{
		$t_current_analysis.empty();
	}
	catch(err)
	{
		//console.log(err);
		
		$t_current_analysis = $('<table></table>',{
			id : "t_current_analysis"
		});
	}
}



