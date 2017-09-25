$(function(){
    var filters = [];
    
    $('.filters .filter').click(function(e) {
	e.preventDefault();
	
	var filterVal = $(this).data('filter');
	var pos = filters.indexOf(filterVal);
	filters = [];
	if (pos == -1) {
	    filters.push(filterVal);
	} else {
	    //filters.splice(pos, 1);
	}

	console.log(filters);
	
	$('.dog-container').each(function() {
	    var item = $(this);
	    var show = false;

	    if (filters.length > 0) {
		$.each(filters, function(key, val) {
		    if (item.data('filter-data').indexOf(val) != -1) {
			show = true;
		    }
		});
	    } else {
		show = true;
	    }
	    
	    if (show) {
		item.show();
	    } else {
		item.hide();
	    }
	});

	$('.filters .filter').each(function () {
	    var item = $(this);

	    if(filters.indexOf(item.data('filter')) == -1) {
		item.removeClass('active');
	    } else {
		item.addClass('active');
	    }
	});
    });
});
