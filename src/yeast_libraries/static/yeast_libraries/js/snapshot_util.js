

function snapshotQuery(plateMap, asJson)
{
    var dataMap = plateMap.dataMap;

	if(plateMap.focused_stack_name === undefined)
	{
		alert('Please choose a library and a copy in the scroll bars on the lower left');

        return false;
 	}
 	else
 	{
        console.log('plateMap.focused_plate: ' , plateMap.focused_plate)

        if(plateMap.focused_plate === undefined)
 		{
 			alert('Please choose a plate');

            return false;
 		}
 		else if(plateMap.focused_plate == 1)
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

        var j = undefined;

        if(asJson === undefined)
        {
            j  = ''.concat('library=', plateMap.focused_lib_name, '&',
                'stack=', plateMap.focused_stack_name, '&', 'stack_pk=', stack_pk,
                '&','plate_num=', (plateMap.focused_plate + 1), '&', 'batch_num=', batch_num);
        }
        else
        {
            j = [];

            j.push(
                {
                    'stack_id': stack_pk,
                    'plate_num': (plateMap.focused_plate + 1),
                    'batch_num': batch_num
                }
            );
        }

		console.log('snapshot query');
		console.log(j);

		return j;
 	}
}