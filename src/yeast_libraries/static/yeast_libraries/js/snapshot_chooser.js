function CopySnapshotMap(context_view) 
{
	this.context_view = context_view;
	this.copy_pk;
	this.map;
	this.plate_maps = [];
	this.total_plates;
	this.focused_plate;
	
	var csm = this;
	
	this.getMap = function (update)
	{	
		$.get( "/yeast_libraries/copy_snapshot_map/" + "?copy_pk=" + csm.copy_pk, function(data) 
        {
        	// console.log('');
        	// console.log('csm.context_view: ', csm.context_view);
            // console.log('callback copy_snapshot_map: ');
            // console.log(data);
            
            csm.map = JSON.parse(data);
            
            csm.initiate(update);
        });
	}; 

	this.initiate = function(update)
    {
    	csm.total_plates = csm.map.length;
    	//console.log('csm.total_plates', csm.total_plates);
    	
    	csm.plate_maps = [];
            
        for(var i=0; i<csm.map.length; i++)
        {
        	var j = csm.map[i];
        	snapshotMap = new PlateSnapshotMap(j['pk']);
        	snapshotMap.initiate(j);
        	
        	csm.plate_maps.push(snapshotMap);
        }
        
        if(csm.map.length > 0)
        {
        	csm.focused_plate = 0;
        }
        else
        {
        	csm.focused_plate = undefined;
        }
        
        //console.log('csm.focused_plate: ', csm.focused_plate);
         
        update(csm);
    };
    	
	
	this.getFocusedSnapshotMap = function()
	{
		return csm.plate_maps[csm.focused_plate];
	};
	
	this.getSnapshotMap = function(plate_num)
	{
		return csm.plate_maps[plate_num - 1];
	};
};

function PlateSnapshotMap(plate_pk)
{
    this.plate_pk = plate_pk;
    this.index;
    this.map;
    this.total_batches;
    this.focused_batch;
    this.total_snapshots;
    this.focused_snapshot;

    var psm = this;

    this.getMap = function (update)
    {
        $.get( "/yeast_libraries/snapshot_map/" + "?plate_pk=" + psm.plate_pk, function(data) 
        {
            // console.log('callback snapshot_map: ');
            // console.log(data);
            
            var map = JSON.parse(data);
            psm.initiate(map);
            
            update(psm);
        });
    };
    
    
    this.initiate = function(map)
    {
    	//console.log('JSON.stringify(map)');
    	//console.log(JSON.stringify(map));
    	
    	psm.map = map;
    	psm.index = map['index'];
        psm.total_batches = psm.map['batches'].length;
        
        //console.log('knock');
        psm.resetBatch();
    };
    
    
    this.resetBatch = function ()
    {
        if(psm.total_batches > 0)
        {
            psm.focused_batch = 0;
            psm.resetSnapshot(psm.focused_batch);
        }
        else
        {
            //console.log('no batches');
            psm.focused_batch = undefined;
            psm.total_snapshots = undefined;
            psm.focused_snapshot = undefined;
            
            return;
        } 
    };
    
    this.resetSnapshot = function(batch_index)
    {
        var batch = psm.map['batches'][batch_index];
        
        if(batch === undefined)
        {
        	psm.total_snapshots = undefined;
        	psm.focused_snapshot = undefined;
        	
        	console.log('no snapshots');
        }
        else
        {
        	var snapshots = batch['snapshots'];
	        psm.total_snapshots = snapshots.length;
	        
	        if(psm.total_snapshots > 0)
	        {
	            psm.focused_snapshot = 0;
	            //console.log(psm.total_snapshots, ' snapshots');
	        }
	        else
	        {
	        	psm.focused_snapshot = undefined;
	        }
        }
        
    };
    
    
    this.nextBatch = function()
    {
        if(psm.total_batches - 1 > psm.focused_batch)
        {
            psm.focused_batch++;
        }
        else
        {
            psm.focused_batch = 0;
        }    
        
        this.resetSnapshot(psm.focused_batch);
        //console.log('focused batch', psm.focused_batch);
    };
    
    this.backBatch = function()
    {
        if(psm.focused_batch > 0)
        {
            psm.focused_batch--;
        }
        else
        {
            psm.focused_batch = psm.total_batches - 1;
        }    
        
        //console.log('focused batch', psm.focused_batch);
        
        this.resetSnapshot(psm.focused_batch);
    };
}


function scoodBatch(dataMap, next)
{	
	//console.log('veritasium mobile');
	var psm = dataMap.getFocusedSnapshotMap();
	
	if(next)
	{
		psm.nextBatch();
	}
	else
	{
		psm.backBatch();
	}
	
	// console.log('psm.focused_batch: ', psm.focused_batch);
	// console.log('psm.total_batches: ', psm.total_batches);
	
	updateBatchGUI(dataMap);
}