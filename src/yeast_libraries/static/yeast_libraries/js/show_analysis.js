

$(document).ready(function()
{
	showHeader();
	showTable();
	createControl();
});


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


