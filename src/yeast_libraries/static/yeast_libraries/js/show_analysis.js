

$(document).ready(function()
{
	showHeader();
	showTable();
	createControl();
});

function showHeader()
{
	header = 'Analysis';
	
	if(type.toString() == 'analyze_over_lib')
	{
		header = 'Image Analysis Over Library Pattern';
	}
	else if(type.toString() == 'analyze')
	{
		header = 'Image Analysis';
	}
	else if(type.toString() == 'lib_pattern')
	{
		header = 'Basic Plate Colony Pattern';
	}
	
	$('#div_header').append('<h1>'+ header + '</h1>');
	$('#div_header').append('<h1>'+ stack + '</h1>');
    $('#div_header').append('<h1> Plate #'+ plate + ' Batch #'+ batch + '</h1>');
}



function showTable()
{	
	console.log('data: ');
	console.log(data.toString());
	console.log('type.toString(): ', type.toString());
	
	$t_current_analysis = $('<table></table>',{
			id : "t_current_analysis",
		});
	
	drawTable();
}

function drawTable()
{
	width = data.length;
	height = data[0].length;
	console.log('width ', width, 'height: ', height);	
		
	tr = $('<tr></tr>', {
			class: "analysis_tr",
			
		});
	
	for(j=0; j<=height; j++)
	{	
		if (j == 0)
		{
			t = '';
		}
		else if(j<10)
		{
			t = '0'+j;
		}
		else
		{
			t = j;
		}
		
		
		td = $('<td></td>', {
			text: t,
			class: "analysis_td_header",
			
		});
	
		tr.append(td); 
	}
	
	$t_current_analysis.append(tr);
	
	for(i=0; i<width; i++)
	{
		letter = String.fromCharCode(97 + i).toUpperCase();
		
		tr = $('<tr></tr>');
		
		td = $('<td class="analysis_td_header">'+ letter +'</td>');
		
		tr.append(td); 

		
		for(j=1; j<=height; j++)
		{
			class_name = 'analysis_row';
			
			pic_locus = data[i][j-1];
			
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
				else if(pic_locus==1)
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
				class: class_name,				
			});	
			tr.append(td); 
		}
		
		$t_current_analysis.append(tr);
	}
	
	$('#div_table').append($t_current_analysis);
}


function createControl()
{
	$b_get_excel = $('<img>',{
		id : "b_get_excel",
		src : "/static/yeast_libraries/img/excel.png",
	    text: 'excel',
	    title: 'excel',
	    href: '#',
	    click: function(){ getAsExcel();}
	});
	
	$('#div_control').append($b_get_excel);
}


function getAsExcel()
{
	console.log('getAsExcel()');
	console.log('get_query', get_query);
	
	
	if(type=='analyze_over_lib')
	{
		location.href="/yeast_libraries/getSnapshotOverLibAnalysis?" + get_query;
	}
	else if(type=='lib_pattern')
	{
		location.href="/yeast_libraries/getSnapshotOverLibAnalysis?" + get_query;
	}
	else if(type=='analyze')
	{
		location.href="/yeast_libraries/getSnapshotAnalysis?" + get_query;				
	}
	else if(type=='compare')
	{
		location.href="/yeast_libraries/compare_snapshots?" + get_query;		
	}
}


