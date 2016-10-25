var addToCourseCart;
setTimeout(function(){
	var titleRaw = $("#banner-info > .title")[0].innerHTML;
	title = titleRaw.substring(0,titleRaw.indexOf("<span")).split("\n").join("");
	instructors = [];
	$("td.col_instructor > a").each(function(i){instructors.push(this.innerHTML.split("\n").join("").trim())});

	var findInstructorData = function(instructor){
		if (instructors.indexOf(instructor) < 0)
			return null;
		var columns = [];
		$("#course-table > thread > tr > th > .th-text").each(function(i){
			if (i > 2) {
				columns.push(this.innerHTML);
			}
		});
		var data = [];
		$("#course-table > tbody > tr.row_display:eq(" + instructors.indexOf(instructor) + ") > td:gt(2) > span.cell_recent").each(
			function(i){
				data.push({category: columns[i], recent: this.innerHTML != "" ? Number(this.innerHTML) : "N/A"});
			});
		
		$("#course-table > tbody > tr.row_display:eq(" + instructors.indexOf(instructor) + ") > td:gt(2) > span.cell_average").each(
			function(i){
				data[i].average = this.innerHTML != "" ? Number(this.innerHTML) : "N/A";
			});
		return {course: title, professor: instructor, info: data};
	}
	var listProfessors = function() {
		var list = "<div id='divList'><ul class='professorList'>";
		var close = "$('[data-original-title]').popover('hide');";
		for (var i = 0; i < instructors.length; i++) {
			list += "<li><button id='" + instructors[i].split(" ").join("") + "' onclick='addToCourseCart(instructors[" + i  +"]);'>" + instructors[i]  + "</button></li>";
		}
		list += "</ul></div>";
		$("#popup").attr("data-content",list);
	}
	
	var addCartButton = function() {
		$("p.subtitle")[0].innerHTML = $("p.subtitle")[0].innerHTML + "<span class='button courseCart'><small id='popup' data-html='true' data-toggle='popover' data-content='' title='Select Professor'><i class='fa fa-cart-plus' aria-hidden='true'></i>  Add to My Cart</small></span>";
		listProfessors();
		$("[data-toggle=popover]").popover();
		$("[data-toggle=popover]").popover('hide');
		$(".courseCart").click(function() {
			$("[data-toggle=popover]").popover();
			listProfessors();
		});
		$('body').on('hidden.bs.popover', function (e) {
			    $(e.target).data("bs.popover").inState = { click: false, hover: false, focus: false }
		});
		$('html').on('click', function(e) {
			if (typeof $(e.target).data('original-title') == 'undefined' && !$(e.target).parents().is('.popover.in')) {
				$('[data-original-title]').popover('hide');
				$('[data-original-title]').popover();
				$('[data-original-title]').popover('hide');
			}
		});
	}
	var addRemoveButton = function() {
		$('.courseCart').remove();
		$('p.subtitle')[0].innerHTML = $('p.subtitle')[0].innerHTML + "<span class='button courseCart'><small id='remove'><i class='fa fa-trash-o'></i> Remove from My Cart</small></span>";
		$('#remove').click(function(){
			$("#remove").remove();
			addCartButton();
			localStorage.removeItem(title);
		});
	}
	addToCourseCart = function(instructor) {
		$('[data-original-title]').popover('hide');
		if (typeof(Storage) !== "undefined") {
			localStorage.setItem(title, JSON.stringify(findInstructorData(instructor)));
			addRemoveButton();
		} else {
			alert("Sorry! Your browser does not support this feature. Please try again with a different browser.");
		}
	}
	if (typeof(Storage) !== "undefined" && localStorage.getItem(title)) {
		addRemoveButton();
	} else {
		addCartButton();
	}
}, 1500);
