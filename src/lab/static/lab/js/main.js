
function hide()
{
	$("#frog").hide();
	alert('knack');
}
    
 
function link(inner_link)
{
	//window.location.href = 'http://127.0.0.1:8000/' + inner_link;
	window.location.href = inner_link;
}


// function link(inner_link)
// {
	// alert(inner_link);
// 	
	// $.get("http://127.0.0.1:8000/?nav="+ inner_link,function(data,status){
    // window.location.href = "/search";
  // });
// }



$(document).ready(function()
{
	csrftoken = getCookie('csrftoken');
    console.log('csrftoken: ', csrftoken)

    createControl($('#div_choice'))

});


function createControl(parent_element)
{

    t_control = $('<table>', {
		id: 't_control',
		class : "c_t_control"
	});

    parent_element.append(t_control)

        tr_control1 = $('<tr>', {
            id: 'tr_control1',
            class : "c_tr_control"
        });

            t_control.append(tr_control1);

                td_control1 = $('<td>', {
                    id: 'td_control1',
                    class : "c_td_control"
                });

                tr_control1.append(td_control1);

                    td_control1.append('<h2>Image Library & Analysis</h2>');

                    img_image_analysis = $('<img>', {

                        id: 'img_image_analysis',
                        class : "control",
                        src: "static/lab/img/snapshot.png",
                        click: function(){link('yeast_libraries/library_copier')}
                    });

                    td_control1.append(img_image_analysis);

                td_control2 = $('<td>', {
                    id: 'td_control2',
                    class : "c_td_control"
                });

                tr_control1.append(td_control2);

                    td_control2.append('<h2>Admin</h2>');

                    img_admin = $('<img>', {

                        id: 'img_plate_img_analysis',
                        class : "control",
                        src: "static/lab/cool1.jpg",
                        click: function(){link('admin/')}
                    });

                    td_control2.append(img_admin);


                td_control3 = $('<td>', {
                    id: 'td_control3',
                    class : "c_td_control"
                });

                tr_control1.append(td_control3);

                    td_control3.append('<h2>Liquid Plate</h2>');
                    td_control3.append('<h2>Growth Analysis</h2>');

                    img_growth = $('<img>', {

                        id: 'img_growth',
                        class : "control",
                        src: "static/yeast_liquid_plates/img/growth.jpeg",
                        click: function(){link('yeast_liquid_plates/liquid_plate_analysis/')}
                    });

                    td_control3.append(img_growth);

                td_control4 = $('<td>', {
                    id: 'td_control4',
                    class : "c_td_control"
                });

                tr_control1.append(td_control4);

                    td_control4.append('<h2>Snapshot</h2>');

                    img_snapshot = $('<img>', {

                        id: 'img_snapshot',
                        class : "control",
                        src: "static/lab/img/snapshot.png",
                        click: function(){link('yeast_libraries/cam/')}
                    });

                    td_control4.append(img_snapshot);

}