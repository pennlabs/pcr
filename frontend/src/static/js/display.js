//create object to convert the property names to html ids
let mode = 'average';
let toGray = [];

let listings = {};
listings.courseBoxOne = 'rCourseQuality';
listings.courseBoxTwo = 'rInstructorQuality';
listings.courseBoxThree = 'rDifficulty';
listings.courseBoxFour = 'rWorkRequired';

//names to be used in the four boxes (length is limited)
const propertyShortNames = {
  rCourseQuality: 'Course', rInstructorQuality: 'Instructor',
  rDifficulty: 'Difficulty', rAmountLearned: 'Learned',
  rWorkRequired: 'Workload', rReadingsValue: 'Reading',
  rCommAbility: 'Instr Comm', rInstructorAccess: 'Access',
  rStimulateInterest: 'Interest', rTAQuality: 'TA Quality',
  rRecommendMajor: 'Major', rRecommendNonMajor: 'Non-Major'
};

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
    //out extraneous info that is stored in localStorage
    if (course && course.info) {

      //run through all the properties in the course
      for (let i = 0; i < course.info.length; i++) {

        //check to see if the class should be included in the average
        if (course.info[i].recent > 0 && !toGray.includes(course.course)) {

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

  //go through each of the properties in listings and set the innerHTML
  //for the appropriate html element corresponding to the data
  //the value input is the average of the property (sum / count)
  for (let property in listings) {
    if (!count[listings[property]]) {
      $("#" + property).html("N/A");
    } else if (mode === 'average') {
      $("#" + property).html((sum_average[listings[property]] /
        count[listings[property]]).toFixed(1));
    } else {
      $("#" + property).html((sum_recent[listings[property]] /
        count[listings[property]]).toFixed(1));
    }
  }
}

//function to display all courses in the box,
//and call update every 1000 ms as well on event
const drawCourses = function() {
  const formCourse =
    function(name, courseQuality, instructorQuality, difficulty, workload) {
      let div = $('<div>');
      div.click(
        function() {
          div.toggleClass('courseInBoxGrayed');
          if (toGray.includes(name)) {
            toGray.splice(toGray.indexOf(name), 1);
          } else {
            toGray.push(name);
          }
          update();
        });
      if (toGray.includes(name)) {
        div.toggleClass('courseInBoxGrayed');
      }
      div.attr('id', name.replace(/ /g, ''));
      div.addClass('tooltip');
      div.addClass('courseInBox');
      let fontAwesome = $('<i>');
      fontAwesome.click(
        function() {
          if (toGray.includes(name)) {
            toGray.splice(toGray.indexOf(name), 1);
          }
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
      innerSpan.append('Course Quality: ' + courseQuality);
      innerSpan.append($('<br>'));
      innerSpan.append('Instructor Quality: ' + instructorQuality);
      innerSpan.append($('<br>'));
      innerSpan.append('Difficulty: ' + difficulty);
      innerSpan.append($('<br>'));
      innerSpan.append('Workload: ' + workload);
      hoverSpan.html(innerSpan.html());
      div.append(hoverSpan);
      return div;
    }
  $('#courseBox').html('');
  for (let key in localStorage) {
    const course = JSON.parse(localStorage.getItem(key));
    let quality;
    let instructor;
    let difficulty;
    let workload;
    if (course && course.info) {
      for (let i = 0; i < course.info.length; i++) {
        if (course.info[i].category === "rCourseQuality") {
          quality = course.info[i].average;
        } else if (course.info[i].category === 'rInstructorQuality') {
          instructor = course.info[i].average;
        } else if (course.info[i].category === 'rDifficulty') {
          difficulty = course.info[i].average;
        } else if (course.info[i].category === 'rWorkRequired') {
          workload = course.info[i].average;
        }
      }
    }
    if (course && course.course) {
      $("#courseBox").append(formCourse(course.course, quality,
        instructor, difficulty, workload));
    }
  }
  $('#categoriesButton').click(function() {
    $('#choose-cols').css('display', 'block');
  });

  //array holding checked checkboxes
  let checked = [];

  //on click of submit
  $('[value=Submit]').click(function() {
    //clear checked
    checked = [];

    //fill checked
    $('.col > p > input:checkbox:checked').map(function() {
      checked.push(this.value);
    });

    //if the user has not selected four categories, do not close
    // and alert them
    if (checked.length < 4) {
      $('#submitCategoriesPopup').css('opacity', 1);
      return;
    } else {
      $('#submitCategoriesPopup').css('opacity', 0);
    }

    //otherwise close the popup
    $('#choose-cols').css('display', 'none');

    //set the new categories to be averaged
    listings.courseBoxOne = checked[0];
    listings.courseBoxTwo = checked[1];
    listings.courseBoxThree = checked[2];
    listings.courseBoxFour = checked[3];

    //change the text in the boxes displaying the averages
    for (let i = 0; i < 4; i++) {
      $('.desc')[i].innerHTML = propertyShortNames[checked[i]];
    }

    update();
  });

  //block of code to make sure no more than 4 are checked at once
  const limit = 4;
  $('.col > p > input').on('change', function() {
    const checked = $('.col > p > input:checked').length
    if (checked > limit) {
      this.checked = false;
    } else if (checked === limit) {
      $("#submitCategoriesPopup").css('opacity', 0);
    }
  });

  update();
  setInterval(update, 1000);
}

//function for closing the choose categories popup
let cancel_choose_cols = function() {
  $('#choose-cols').css('display', 'none');
}

const set_datamode = function(n) {
  if (n === 1) {
    $('#view_average').removeClass('selected');
    $('#view_recent').addClass('selected');
    mode = 'recent';
  } else if (n === 0) {
    $('#view_average').addClass('selected');
    $('#view_recent').removeClass('selected');
    mode = 'average';
  }
  update();
}

const display = function() {

  $("#choose-cols-content > div > p > input").click(
    function() {
      let clicked = 0;
      $("#choose-cols-content > div > p > input").each(
        function() {
          clicked += $(this).prop('checked') ? 1 : 0;
        });
    });

  //set the defaults to be checked
  $('[name=rDifficulty]').prop('checked', true);
  $('[name=rCourseQuality]').prop('checked', true);
  $('[name=rInstructorQuality]').prop('checked', true);
  $('[name=rWorkRequired]').prop('checked', true);

  $('#submitCategoriesPopup').css('opacity', 0);
  drawCourses();
  window.addEventListener('storage', drawCourses);
}
