



function showHeader()
{
	var header = 'Analysis';
	
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
	$('#div_header').append('<h1>'+ stack + ' Plate #'+ (plate + 1) + ' Batch #' + (batch + 1) + '</h1>');


    $div_legend = $('#div_legend');
}


function showLegend(parentElement)
{
    $t_legend = $('<table></table>', {
        id : "t_legend"
    });

    parentElement.append($t_legend);

        var tr = $('<tr></tr>', {
			class: "tr_legend"
		});

            var td = $('<td class="td_legend"></td>');

            td.append($('<img>', {

                src: "/static/yeast_libraries/img/colony.png"
            }));

            tr.append(td);

            td = $('<td class="td_legend">'+ 'Pattern congruent colony' +'</td>');

            tr.append(td);


        $t_legend.append(tr);

        tr = $('<tr></tr>', {
			class: "tr_legend"
		});

            td = $('<td class="td_legend"></td>');

            td.append($('<img>', {

                src: "/static/yeast_libraries/img/contamin.png"
            }));

            tr.append(td);

            td = $('<td class="td_legend">'+ 'Contaminated' +'</td>');

            tr.append(td);


        $t_legend.append(tr);


        tr = $('<tr></tr>', {
			class: "tr_legend"
		});

            td = $('<td class="td_legend"></td>');

            td.append($('<img>', {

                src: "/static/yeast_libraries/img/extinct.png"
            }));

            tr.append(td);

            td = $('<td class="td_legend">'+ 'Extinct' +'</td>');

            tr.append(td);

//            td = $('<td class="td_legend"></td>');
//
//                td.append('<h1>Yooohhho Ha</h1>')
//
//            tr.append(td);


        $t_legend.append(tr);
}


function showTable()
{	
	console.log('data: ');
	console.log(data.toString());
	console.log('type.toString(): ', type.toString());
	
	$t_current_analysis = $('<table></table>', {

        id : "t_current_analysis"
    });

	$('#div_table').append($t_current_analysis);

	drawTable($t_current_analysis, $div_legend, type, data);
}

function drawTable(parentTable, parentLegend, type, data)
{
	var width = data.length;
	var height = data[0].length;
	console.log('width ', width, 'height: ', height);	

    if(type=='analyze_over_lib')
    {
        showLegend(parentLegend);
    }

	var tr = $('<tr></tr>', {
			class: "analysis_tr"
			
		});

    var td;

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
			class: "analysis_td_header"
			
		});
	
		tr.append(td); 
	}
	
	parentTable.append(tr);

    var pic_locus;
    var lib_locus;
    var letter;
	
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
                console.log('pic_locus: ', pic_locus)

				if(pic_locus==0)
				{
					pic_locus = 'V';
                    class_name = 'td_comparison_congruent_full'
				}
				else if(pic_locus==1)
				{
					pic_locus = 'X';
                    class_name = 'td_comparison_discrepancy_extinct';
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

            if(type=='analyze_over_lib')
            {

                if(class_name == 'analysis_td_true_positive')
                {

                    td.append($('<img>', {

                        class: "colony",
                        src: "/static/yeast_libraries/img/colony.png",
                        click: function(){alert("Colony in library and in image")}
                    }));
                }
                else if(class_name == 'analysis_td_false_positive')
                {
                    td.append($('<img>', {

                        class: "colony",
                        src: "/static/yeast_libraries/img/contamin.png",
                        click: function(){alert("A colony contaminated empty cell")}
                    }));
                }
                else if(class_name == 'analysis_td_false_negative')
                {
                    td.append($('<img>', {

                        class: "colony",
                        src: "/static/yeast_libraries/img/extinct.png",
                        click: function(){alert("The library colony is extinct")}
                    }));
                }
                else
                {
                    td.append($('<img>', {

                        class: "colony",
                        src: "/static/yeast_libraries/img/true_negative.png",
                        click: function(){alert("Empty in library and in image")}
                    }));
                }
            }
		}
		
		parentTable.append(tr);
	}
}


