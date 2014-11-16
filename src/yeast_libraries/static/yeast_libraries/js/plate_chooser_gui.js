

function createCurrent(parent_element, plateMap, update)
{	
	$t_current = $('<table id="t_current"></table>');
	
		createCurrentControl($t_current, plateMap, update); 
		
			$td_current_img = $('<td id = "td_current_img", class="td_reg_flow"></td>');
			
				$img_current = $('<img src="/static/yeast_libraries/img/384_0001.jpg", width="600", height="400"></img>');		
				$td_current_img.append($img_current);

                    $b_show_unprocessed = $('<input>', {
                        type: "button",
                        id : "$b_show_processed",
                        class: "b_processed",
                        value: "View Unprocessed",
                        click: function()
                        {
                            if(this.value == "View Unprocessed")
                            {
                                showImage(plateMap.dataMap, false);
                                this.value = "View Processed";
                            }
                            else
                            {
                                showImage(plateMap.dataMap, true);
                                this.value = "View Unprocessed";
                            }

                        }
                    }
                );


                $td_current_img.append('<br>');
                $td_current_img.append($b_show_unprocessed);

		
		$t_current.append($td_current_img);
	
	parent_element.append($t_current);
}



function createCurrentControl(parent_element, plateMap, update)
{
	$td_current_control = $('<td id="td_current_control", class="td_reg_flow"></td>');
	$td_current_control.append('<h1 class="control_header">Plate</h1>');
	
	$td_current_control.append('<h2 class="control_label">Library</h2>');
	$td_current_control.append('<select id="library_list", class="control_select" multiple>');
	
	$td_current_control.append('<h2 class="control_label">Copy</h2>');
	$td_current_control.append('<select id="stack_list" multiple></select>');	
	

	$div_snapshot_control = $('<div id="div_snapshot"></div>');
	
		$plate_counter = $('<h2 class="control_label">No Plates A</h2>');
		$div_snapshot_control.append($plate_counter);
	
		$browser = $('<div id="browser"></div>');
		
		$div_snapshot_control.append($browser);
		
		$img_back = $('<img>',{
			id : "back",
			src : "/static/yeast_libraries/img/back.png",
		    text: 'Back',
		    title: 'Back',
		    href: '#',
		    click: function(){console.log('hame haye'); plateMap.backPlate(update);}
		});
		
		$browser.append($img_back);
		
		
		$img_next = $('<img>',{
			id : "next",
			src : "/static/yeast_libraries/img/next.png",
		    text: 'Next',
		    title: 'Next',
		    href: '#',
		    click: function(){ plateMap.nextPlate(update);}
		});
		
		$browser.append($img_next);
		
	$td_current_control.append($div_snapshot_control);
		
	parent_element.append($td_current_control);
}