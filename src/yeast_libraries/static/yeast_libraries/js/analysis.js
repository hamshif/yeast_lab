
$(document).ready(function()
{
	createComparisonGui();
	
});


function createComparisonGui()
{	
	$t_frame = $('<table></table>');
		
		$tr_comparison = $('<tr></tr>');
			
			$td_current = $('<td></td>');
			
				$t_current.append('<h2>Current Stack</h2>');
					
				
				$td_current.append($t_current_control);
					
				$img_current = $('<img src="/static/yeast_libraries/img/384_0001.jpg" width="600", height="400"></img>');
				
				$td_current.append($img_current);

			
			$tr_comparison.append($td_current);
			
			$td_compared = $('<td></td>');
					
				$img_compared = $('<img src="/static/yeast_libraries/img/384_0002.jpg" width="600", height="400"></img>');
				
				$td_compared.append($img_compared);
			
			$tr_comparison.append($td_compared);	
	
	$t_frame.append($tr_comparison);
		
		$tr_results = $('<tr></tr>');
	

	$(':eq(0)').append($t_frame);
	
	//$t_frame.hide();
}
