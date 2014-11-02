

function LibraryFilter(plateMap)
{
	this.plateMap = plateMap;
	
	this.getMap = function (select_element)
	{
		$.ajax
		(
			{ 
				url: "/yeast_libraries/private_lib_list/", 
				success: function(response)
				{
					select_element.empty();
					//console.log('callback: /yeast_libraries/private_lib_list/', response);
					var personal_names = JSON.parse(response);
					//console.log('personal_names: ', personal_names);
					
					$s_users.append($('<option>',{
						text: COMMON_USER,
						value: COMMON_USER,	
					}));
					
					for(i=0; i < personal_names.length; i++)
					{
						select_element.append($('<option>',{
							text: personal_names[i],
							value: personal_names[i],
						}));
						
						select_element.multiSelect('refresh');
					}
				}
			}
		);
	};
}



function createLibFilter(parent_element, plateMap)
{
	$td_search = $('<td>', {
		
		id: "td_search",
		class: "td_reg_flow",
	});
	
	parent_element.append($td_search);	
	
		$td_search.append($('<h1 class="control_label">Filter Libraries<h1>'));
		
		$td_search.append($('<h2 class="control_label">nicknames<h2>'));
		
		$s_users = $('<select multiple>', {
			id: "s_users",
			class: "control_select",
		});
		
		
		$td_search.append($s_users);

		$td_search.append('<br></br');
	
		$b_filter_libs = $('<input>', {
			
			id: "b_filter_libs",
			type:"button",
			value: "Filter",
			click: function()
			{
				//console.log('$s_users.val(): ', $s_users.val());
				if($s_users.val() == null)
				{
					confirm("Please choose at least one user name");
				}
				else
				{
					//console.log('updatePlateChoosingGUI: ', updatePlateChoosingGUI);
					plateMap.getMap($s_users.val(), true, updatePlateChoosingGUI);
				}
				
			},
		});
		
		$td_search.append($b_filter_libs);
}