var update = function() {
		var sum_recent = {};
		var sum_average = {};
		var count = {};
		for (var key in localStorage) {
			var course = JSON.parse(localStorage.getItem(key));
			if (course.info) {
				for (var i = 0; i < course.info.length; i++) {
					if (course.info[i].recent >= 0 && !$("#" + course.course.split(" ").join("")).hasClass("courseInBoxGrayed")) {
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
		var listings=[["rCourseQuality","courseNum"],["rInstructorQuality","instructorNum"],["rDifficulty","difficultyNum"],["rWorkRequired","workloadNum"]];
		for (var i = 0; i < listings.length; i++) {
			if (count[listings[i][0]]) {
				$("#"+listings[i][1])[0].innerHTML=(sum_average[listings[i][0]]/count[listings[i][0]]).toFixed(1); 
			} else {
				$("#"+listings[i][1])[0].innerHTML= "0.0";
			}
		}
	}
var display = function() {	
	var formCourse = function(name, v1, v2, v3, v4) {
		var nospaces = name.split(" ").join("");
		var html = "<div onclick='$(\"#" + nospaces + "\").toggleClass(\"courseInBoxGrayed\"); update();'"
			+ "id='"+ nospaces +"' class='tooltip courseInBox'>"
			+ '<i onclick="$(\'#'+ nospaces + '\').remove();localStorage.removeItem(\'' + name + '\');update();" class="fa fa-times" aria-hidden="true"></i>'
			+ name + '<span class="tooltiptext">' + "Course Quality: " + v1 + "<br> Instructor Quality: " + v2 + "<br> Difficulty: " + v3 + "<br> Workload: "
			+ v4 + "</span>" + "</div>";
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
				if (course.info[i].category == "rCourseQuality") {
					quality = course.info[i].average;
				} else if (course.info[i].category == "rInstructorQuality") {
					instructor = course.info[i].average;
				} else if (course.info[i].category == "rDifficulty") {
					difficulty = course.info[i].average;
				} else if (course.info[i].category == "rWorkRequired"){
					workload = course.info[i].average;
				}
			}
		}
		if (course.course)
			$("#courseBox").html($("#courseBox").html() + formCourse(course.course, quality, instructor, difficulty, workload));
	}	
	update();
	setInterval(update, 1000);
}
