
function PlatePattern()
{
	this.copy_pk;
	this.plate_pk; 
	this.map;
	this.width;
	this.height;
	
	this.saved_cells = {};
	//console.log('PlatePattern');
}


PlatePattern.prototype.getMap = function(copy_pk, plate_pk, update)
{
	//console.log('PlatePattern.prototype.getMap');
	this.copy_pk = copy_pk;
	this.plate_pk = plate_pk;
	var pp = this;
	
	this.verifyKey();
	
	
	$.get( "/yeast_libraries/get_plate_pattern/?plate_pk=" + plate_pk, function(data) 
	{
		//console.log('/yeast_liquid_plates/get_spectrometer_experiments/: ');
		//console.log(data);
		
		var j = JSON.parse(data);
		pp.map = j['loci'];
		// console.log('pp.map: ');
		// console.log(JSON.stringify(pp.map));
		
		pp.width = j['width'];
		pp.height = j['height'];
		
		update(pp);
	});
};


PlatePattern.prototype.clear_choice = function(updateCellChooserGUI)
{
    var keys = Object.keys(this.saved_cells);
    var key;

    for(var i in keys)
    {
        key = keys[i];

        console.log('key: ', key);
        this.saved_cells[key] = {};
    }

    updateCellChooserGUI(this);
	console.log('PlatePattern');
};



PlatePattern.prototype.createPlateKey = function()
{
	if(this.copy_pk == undefined || this.plate_pk == undefined)
	{
		return undefined;
	}
	
	return this.copy_pk + 'p' + this.plate_pk;
};


PlatePattern.prototype.verifyKey = function()
{
	var plate_key = this.createPlateKey();
	
	if(plate_key in this.saved_cells)
	{
		//console.log('this.saved_cells[plate_key]: ', this.saved_cells[plate_key]);
	}
	else
	{
		this.saved_cells[plate_key] = {};
	}
};


PlatePattern.prototype.focusOrUnFocusCell = function(id_)
{
	var plate_key = this.createPlateKey();
	
	if(id_ in this.saved_cells[plate_key])
	{
		delete this.saved_cells[plate_key][id_];
		
		//console.log('just unfocused ' + id_);
		console.log('JSON.stringify(this.saved_cells): ' + JSON.stringify(this.saved_cells));
		return false;
	}
	else
	{
		this.saved_cells[plate_key][id_] = id_.split('i');
		//console.log('just focused ' + id_);
		console.log('JSON.stringify(this.focused_cells): ' + JSON.stringify(this.saved_cells));
		return true;
	}
};




PlatePattern.prototype.getCellsGrowth = function()
{	
	var pp = this;

    console.log(JSON.stringify(pp.saved_cells));

    if(Object.keys(pp.saved_cells).length === 0)
    {
        alert('No cells have been chosen!');
        return;
    }

    var cells_chosen = false;

    var keys = Object.keys(pp.saved_cells);
    var key;
    console.log('keys: ', keys);

    for(var i in keys)
    {
        key = keys[i];
        console.log('key: ', key);

        if(Object.keys(pp.saved_cells[key]).length > 0)
        {
            cells_chosen = true;
            break;
        }
    }

    if(!cells_chosen)
    {
        alert('No cells have been chosen!');
        return;
    }

	
	$.ajax({
	    url: '/yeast_liquid_plates/growth_graphs/',
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(pp.saved_cells),
	    //data: experiment,
	    dataType: 'html',//'json',
	    success: function(result) {
	        
//	        console.log(result);
//
//            console.log("");
//            console.log(typeof result);
            $div_plot.empty();
            $div_plot.append(result);

	    }
	});	
};




function createCellChooser(platePattern, parentElement)
{	
	//console.log('createCellChooser');
	
	if(platePattern == undefined || platePattern.map == undefined)
	{
//		console.log('platePattern.map == undefined');
		parentElement.empty();
		
		var width = 24;
		var height = 16;
		
	}
	else
	{
		var width = platePattern.width;
		var height = platePattern.height;
	}
	
	//var p = platePattern.map;
	
	
	//console.log('width: ', width, 'height: ', height);
	
	
	var t_cell_chooser = $('<table></table>',{
			id : "t_cell_chooser"
	});
	
		
	var tr = $('<tr></tr>');
	
	for(var j=0; j<=width; j++)
	{	
		var t = '';
		
		if (j == 0)
		{
			
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
	
	t_cell_chooser.append(tr);
	
	for(var i=0; i<height; i++)
	{
		var letter = String.fromCharCode(97 + i).toUpperCase();
		
		tr = $('<tr></tr>');
		
		td = $('<td class="analysis_row">'+ letter +'</td>');
		
		tr.append(td); 
		
		for(var j=0; j<width; j++)
		{
			var class_name = 'unchecked_cell';			
			var id_ = i + 'i' + j;
			
			var text_ = 'STAM';
			
			if(platePattern != undefined)
			{
				text_ = platePattern.map[i][j]["strain"];
			}
			
			td = $('<td></td>', {
				id: id_,
				text: text_,
				class: class_name,
				click: function(){cellClick(platePattern, this.id);}
				//click: function(){;},		
			});
				
			tr.append(td); 
		}
		
		t_cell_chooser.append(tr);
	}
	
	parentElement.append(t_cell_chooser);
}


function cellClick(platePattern, id)
{
	platePattern.focusOrUnFocusCell(id);
	//console.log('cellClick(): ', id);
	
	var cell = $('#'+id);
	cell.toggleClass('unchecked_cell checked_cell');
}

