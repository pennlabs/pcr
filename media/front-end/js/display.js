//check which values are to be included in the average,
//calculate the average of quality, instructor quality, 
//difficulty, workload and then set the values of the 
//boxes to the new average
const update = function() {
  //objects holding the sums of each proprty within courses 
  let sum_recent = {};
  let sum_average = {};
  //holds the count for each property in the courses
  let count = {};

  //run through the courses in localStorage
  for (let key in localStorage) {
    
    //get the object for the course stored in localStorage
    const course = JSON.parse(localStorage.getItem(key));

    //check to make sure that it is an actual object to filter
    //out extraneous info that is storage in localStorage
    if (course.info) {

      //run through all the properties in the course
      for (let i = 0; i < course.info.length; i++) {

        //check to see if the class should be included in the average
        if (course.info[i].recent >= 0 && !$("#" + 
          course.course.replace(/ /g, '')).hasClass("courseInBoxGrayed")) {
	  
	  //add it to the sum to be averaged
          if (sum_recent[course.info[i].category]) {
            sum_recent[course.info[i].category] += course.info[i].recent;
            sum_average[course.info[i].category] += course.info[i].average;
          } else {
            sum_recent[course.info[i].category] = course.info[i].recent;
            sum_average[course.info[i].category] = course.info[i].average;
          }

	  //increase/set the count for each property
          const cat = count[course.info[i].category];
          count[course.info[i].category] = cat ? cat + 1 : 1;
        }
      }
    }
  }

  //create object to convert the property names to html ids
  let listings={};
  listings.rCourseQuality = "courseNum";
  listings.rInstructorQuality = "instructorNum";
  listings.rDifficulty = "difficultyNum";
  listings.rWorkRequired = "workloadNum";

  //go through each of the properties in listings and set the innerHTML
  //for the appropriate html element corresponding to the data
  //the value input is the average of the property (sum / count)
  for (let property in listings) {
    if (!count[property]) {
      $("#" + listings[property]).html("0.0");
    } else {
      $("#" + listings[property]).html((sum_average[property] / 
                 	                count[property]).toFixed(1));
    }
  }
}

//function to display all courses in the box,
//and call update every 1000 ms as well on event
const display = function() {  
  const formCourse = 
    function(name, courseQuality, instructorQuality, difficulty, workload) {
      let div = $('<div>');
      div.click(
        function() {
          div.toggleClass('courseInBoxGrayed');
          update();
        });
      div.attr('id', name.replace(/ /g, ''));
      div.addClass('tooltip');
      div.addClass('courseInBox');
      let fontAwesome = $('<i>');
      fontAwesome.click(
        function() {
          div.remove();
          localStorage.removeItem(name);
        });
      fontAwesome.addClass('fa');
      fontAwesome.addClass('fa-times');
      fontAwesome.attr('aria-hidden', 'true');
      div.append(fontAwesome);
      div.append(' ' + name);
      let hoverSpan = $('<span>');
      hoverSpan.addClass('tooltiptext');
      let innerSpan = $('<div>');
      innerSpan.append("Course Quality: " + courseQuality);
      innerSpan.append($('<br>'));
      innerSpan.append("Instructor Quality: " + instructorQuality);
      innerSpan.append($('<br>'));
      innerSpan.append("Difficulty: " + difficulty);
      innerSpan.append($('<br>'));
      innerSpan.append("Workload: " + workload);
      hoverSpan.html(innerSpan.html());
      div.append(hoverSpan);
      return div;
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
      $("#courseBox").append(formCourse(course.course, quality, 
			     instructor, difficulty, workload));
    }
  }  
  update();
  setInterval(update, 1000);
}
