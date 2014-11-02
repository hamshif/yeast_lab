
// using different syntax for inner methods


function ExperimentChooser(context_view, plateMap)
{
	this.context_view = context_view;
	this.plateMap = plateMap;
	this.experiments;
}

ExperimentChooser.prototype.getExperiments = function (user, experimentClicked)
{
	var ec = this;
	
	$.get( "/yeast_liquid_plates/get_spectrometer_experiments/?user=" + user, function(data) 
	{
		//console.log('/yeast_liquid_plates/get_spectrometer_experiments/: ',  data);
		
		ec.experiments = JSON.parse(data);
		$select_liquid_experiments.empty();
			
		for(var lib_key in ec.experiments)
		{	
			var copy_dict = ec.experiments[lib_key];
			
			for(var copy_key in copy_dict)
			{
				var plate_dict = copy_dict[copy_key];
				
				//console.log('   JSON.stringify(plate_dict): ', JSON.stringify(plate_dict));
				
				for(var plate_key in plate_dict)
				{	
					var experiments = plate_dict[plate_key];
					
					//console.log('   JSON.stringify(experiments): ', JSON.stringify(experiments));
					
					for(var i = 0; i<experiments.length; i++)
					{
						var experiment = experiments[i];
						experiment['lib_id'] = lib_key;
						experiment['copy_id'] = copy_key;
						experiment['plate_id'] = plate_key;
						
						
						//console.log('               JSON.stringify(experiment): ', JSON.stringify(experiment));
						
						
						$select_liquid_experiments.append(
							$('<option>',{
							value : JSON.stringify(experiment),
							text : experiment.name,
							//click: function(){ console.log(this.value, this.text); ec.showGrowthGraph(experiment);},
							click: function()
								{ 
									experimentClicked(JSON.parse(this.value), ec.plateMap);
								},
							})
						);
							
					}
				}	
			}
		}
		
		update(data);
		
		if(ec.experiments.length > 0)
		{
			$select_liquid_experiments.get(0).options[0].selected = true;
			$select_liquid_experiments.get(0).options[0].click();
		}
	});
};


ExperimentChooser.prototype.showGrowthGraph = function(experiment)
{
	$.ajax({
	    url: '/yeast_liquid_plates/growth_graph/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(experiment),
	    //data: experiment,
	    dataType: 'json',
	    success: function(result) {
	        alert(result.Result);
	    }
	});	
};



ExperimentChooser.prototype.createChooserGUI = function (parent_element)
{
	//console.log('parent_element', parent_element);
	
	parent_element.append('<h1>Registered Experiments</h1>');
	parent_element.append('<h2>Spectrometer</h2>');
	
	$select_liquid_experiments = $('<select multiple>', {
		id: "s_liquid_experiments",

	});
	
	parent_element.append($select_liquid_experiments);
};


ExperimentChooser.prototype.addExperiments = function (experiments)
{
	console.log('experiments', JSON.stringify(experiments));
	//console.log('this.experiments.length: ', this.experiments.length);
	
	for(var key_ in experiments)
	{
		var experiment = experiments[key_];
		
		this.experiments[key_] = experiment;
		
		$select_liquid_experiments.append(
			$('<option>',{
			value : experiment.id,
			text : experiment.name,
			click: function()
				{ 
					console.log(this.value, this.text);
				
				},
			})
		);
	}
};
