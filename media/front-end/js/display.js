var display = function() {
	var formCourse = function(name, v1, v2, v3, v4) {
		var nospaces = name.split(" ").join("");
		var html = "<div onclick='$(\"#" + nospaces + "\").toggleClass(\"courseInBoxGrayed\")'"
			+ "id='"+ nospaces +"' class='tooltip courseInBox'>"
			+ '<i onclick="$(\'#'+ nospaces + '\').remove();localStorage.removeItem(\'' + name + '\')" class="fa fa-times" aria-hidden="true"></i>'
			+ name
			+ '<span class="tooltiptext">'
			+ "Course Quality: " 
			+ v1
			+ "<br> Instructor Quality: " 
			+ v2 
			+ "<br> Difficulty: " 
			+ v3
			+ "<br> Workload: "
			+ v4
			+ "</span>"
			+ "</div>";
		return html;
	}

	for (var key in localStorage) {
		var course = JSON.parse(localStorage.getItem(key));
		var quality;
		var instructor;
		var difficulty;
		var workload;
		if (course.info) {
			for (var i = 0; i < course.info.length; i++) {
				if (course.info[i].category == "Course Quality") {
					quality = course.info[i].average;
				} else if (course.info[i].category == "Instructor Quality") {
					instructor = course.info[i].average;
				} else if (course.info[i].category == "Difficulty") {
					difficulty = course.info[i].average;
				} else if (course.info[i].category == "Amount of Work"){
					workload = course.info[i].average;
				}
			}
		}
		if (course.course)
			$("#courseBox").html($("#courseBox").html() + formCourse(course.course, quality, instructor, difficulty, workload));
	}

	setInterval(function() {
		var sum_recent = {};
		var sum_average = {};
		var count = {};
		for (var key in localStorage) {
			var course = JSON.parse(localStorage.getItem(key));
			var quality;
			var instructor;
			var difficulty;
			var workload;
			if (course.info) {
				for (var i = 0; i < course.info.length; i++) {
					if (course.info[i].recent >= 0 && course.info[i].average >= 0 && !$("#" + course.course.split(" ").join("")).hasClass("courseInBoxGrayed")) {
						if (sum_recent[course.info[i].category]) {
							sum_recent[course.info[i].category] += course.info[i].recent;
							sum_average[course.info[i].category] += course.info[i].average;
						} else {
							sum_recent[course.info[i].category] = course.info[i].recent;
							sum_average[course.info[i].category] = course.info[i].average;
						}
						count[course.info[i].category] = count[course.info[i].category] ? count[course.info[i].category] + 1 : 1;
					}
				}
			}
		}
		var listings=[["Course Quality","courseNum"],["Instructor Quality","instructorNum"],["Difficulty","difficultyNum"],["Amount of Work","workloadNum"]];for(var l in listings)count["Course Quality"]&&($("#"+listings[l][1])[0].innerHTML=(sum_recent[listings[l][0]]/count[listings[l][0]]).toFixed(1)); 
	}, 1000);
}
