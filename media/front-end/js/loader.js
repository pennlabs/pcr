//variable holding the content of the popover
var popoverContent = null;

//function to list professors when there are <= 15
const listProfessors = function() {
  var outerDiv = $('<div>');
  outerDiv.attr('id', 'divList');
  var listOfProfessors = $('<ul>');
  listOfProfessors.addClass('professorList');
  for (var i = 0; i < COURSE_DATA.instructors.length; i++) {
    var prof = COURSE_DATA.instructors[i];
    var listItem = $('<li>');
    var button = $('<button>');
    button.click(
      function(){
        addToCourseCart(prof);
      });
    button.append(prof);
    listItem.append(button);
    listOfProfessors.append(listItem);
  }
  outerDiv.append(listOfProfessors);
  popoverContent = outerDiv;
}

/* purpose of this function is to create
 * a grid of the alphabet to filter profs
 * and display filtered profs*/
const listAlphabet = function(c) {
  var head = $('<p>')
  head.text("Filter by Last Name: ");
  var table = $('<table>');
  table.addClass("professorList");
  var tr = $('<tr>');

  //create the grid of buttons of the alphabet
  for (var i = 1; i <= 26; i++) {
    const character = String.fromCharCode(i+64)
    var button = $('<button>');
    button.text(character);
    var td = $('<td>');

    /*check to see if instructors exist with a last name starting with 'character'
    If so, leave the button clickable and functional; otherwise, gray it out.*/
    
    
    if (!COURSE_DATA.instructors.reduce(
                     function (a,b) { return b.split(" ").pop()[0] == character || a }, false)) {
      button.addClass('grayedOut');
    } else {
      button.click(
        function() {
          $('#filteredProfs').html('');
          listAlphabet(character);
        });
    }
    td.append(button);
    tr.append(td);
    //break for alphabet grid
    if (i%6 == 0) {
      table.append(tr);
      tr = $('<tr>')
    }
  }
  table.append(tr);
  filteredProfs = $('<div>');
  filteredProfs.attr('id', 'filteredProfs');
  table.add(filteredProfs);
  head.add(table);

  //if we have passed in a character, we will search for professors
  //whose last names start with that letter and add them to the list
  if (c) {

     /*check to see if instructors exist with a last name starting with 'character'
    If so, leave the button clickable and functional; otherwise, gray it out.*/
    listOfProfessors =
      COURSE_DATA.instructors.reduce(
        function(a, b) {
          if (b.split(" ").pop()[0] == c) {
            var listItem = $('<li>');
            var button = $('<button>');
            button.attr('id', b.replace(/ /g, ''));
            button.click(
              function() {
                addToCourseCart(b);
              });
            button.append(b);
            listItem.append(button);
            a.append(listItem);
            return a;
          } else {
            return a;
          }
        }, $('<ul>').addClass('professorList'));
    $('#filteredProfs').append(listOfProfessors);
    $("div.arrow").css("top", "103px");
  }
  popoverContent = $('<span>').append(head).append(table).append(filteredProfs);
}

//put the cart button under the scoreboxes
//fill the popover with professors/filtering interface
const addCartButton = function() {
  var addSpan = $('<span>');
  addSpan.addClass('button');
  addSpan.addClass('courseCart');

  var addSmall = $('<small>');
  addSmall.attr('id', 'popup');
  addSmall.attr('data-html', 'true');

  var fontAwesome = $('<i>');
  fontAwesome.addClass('fa');
  fontAwesome.addClass('fa-cart-plus');
  fontAwesome.attr('aria-hidden', 'true');
  addSmall.append(fontAwesome);
  addSmall.append(" Add to My Cart");
  addSpan.append(addSmall);
  $('#banner-score').append(addSpan);

  if (COURSE_DATA.instructors.length <= 15)
    listProfessors();
  else
    listAlphabet(null);

  $('.courseCart').click(function() {
    $('#popup').popover({title: "Select Professor", content: popoverContent, placement: "left"});
    $('#popup').popover('show');
    if (COURSE_DATA.instructors.length <= 15)
      listProfessors();
    else
      listAlphabet(null);
  });
  $('html').on('click', function(e) {

    //if click outside the cart close it.
    if (typeof $(e.target).data('original-title') == 'undefined' &&
        !$(e.target).is('button')  &&
        !$(e.target).parents().is('.popover.in')) {

      //must be toggled twice to avoid having to click twice when opening again
      $('[data-original-title]').popover('hide');
      $('[data-original-title]').popover();
      $('[data-original-title]').popover('hide');
    }
  });
}

//remove the addCart button and replace it
//with a remove from cart option
const addRemoveButton = function() {
  $('.courseCart').remove();
  var removeSpan = $('<span>');
  var removeSmall = $('<small>');
  removeSmall.attr('id', 'remove');
  var fontAwesome = $('<i>');
  fontAwesome.addClass('fa');
  fontAwesome.addClass('fa-trash-o');
  removeSmall.append(fontAwesome);
  removeSmall.append(" Remove from My Cart");
  removeSmall.click(
    function() {
      removeSmall.remove();
      addCartButton();
      localStorage.removeItem(title);
    });
  removeSpan.append(removeSmall);
  $('#banner-score').append(removeSpan);
}

//when a professor is selected, add the remove button and
//add the class to localStorage. If the user's browser cannot
//handle localStorage usage, alert them.
addToCourseCart = function(instructor) {
  $('[data-original-title]').popover('hide');
  if (typeof(Storage) !== "undefined") {
    localStorage.setItem(title,
  JSON.stringify(COURSE_DATA.instructor_data[instructor]));
    addRemoveButton();
  } else {
    alert("Sorry! Your browser does not support this feature." +
        " Please try again with a different browser.");
  }
}
