const update = function() {
    let sum_recent = {};
    let sum_average = {};
    let count = {};
    for (let key in localStorage) {
      const course = JSON.parse(localStorage.getItem(key));
      if (course.info) {
        for (let i = 0; i < course.info.length; i++) {
         //check to see if the class should be included in the average
        if (course.info[i].recent >= 0 && !$("#" + 
            course.course.replace(/ /g,'')).hasClass("courseInBoxGrayed")) {
	    //add it to the sum to be averaged
            if (sum_recent[course.info[i].category]) {
              sum_recent[course.info[i].category] += course.info[i].recent;
              sum_average[course.info[i].category] += course.info[i].average;
            } else {
              sum_recent[course.info[i].category] = course.info[i].recent;
              sum_average[course.info[i].category] = course.info[i].average;
            }
	    //take the sum of each property and count
            const cat = count[course.info[i].category];
            count[course.info[i].category] = cat ? cat + 1 : 1;
          }
        }
      }
    }
    let listings={};
    listings.rCourseQuality = "courseNum";
    lsitings.rInstructorQuality = "instructorNum";
    lisitings.rDifficulty = "difficultyNum";
    listings.rWorkRequired = "workloadNum";

    //go through each of the properties in listings and set the innerHTML
    //for the appropriate html element corresponding to the data
    //the value input is the average of the property (sum / count)
    for (let property in listings) {
      if (listings.hasOwnProperty(property)) {
        $("#" + listings[property]).html(sum_average[listings[property]] / 
			                 count[listings[property]]).toFixed(1);
      }
    }
  }
const display = function() {  
    const formCourse = function(name, courseQuality, instructorQuality, difficulty, workload) {
                          const nospaces = name.split(" ").join("");
                          const html = "<div onclick='$(\"#" + nospaces + 
                            "\").toggleClass(\"courseInBoxGrayed\"); update();'" +
                            "id='" + nospaces + "' class='tooltip courseInBox'>" +
                            '<i onclick="$(\'#'+ nospaces + 
                            '\').remove();localStorage.removeItem(\'' +
                            name + '\');update();" class="fa fa-times" aria-hidden="true"></i>' +
                            name + '<span class="tooltiptext">' + "Course Quality: " +
                            courseQuality + "<br> Instructor Quality: " + instructorQuality + 
                            "<br> Difficulty: " + difficulty + "<br> Workload: "
                            + workload + "</span>" + "</div>";
    return html;
  }

  for (let key in localStorage) {
    const course = JSON.parse(localStorage.getItem(key));
    let quality;
    let instructor;
    let difficulty;
    let workload;
    if (course.info) {
      for (let i = 0; i < course.info.length; i++) {
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
    if (course.course) {
      $("#courseBox").html($("#courseBox").html() + 
        formCourse(course.course, quality, instructor, difficulty, workload));
    }
  }  
  update();
  setInterval(update, 1000);
}
