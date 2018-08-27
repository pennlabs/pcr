//variable holding the content of the popover
var popoverContent = null;

// function to titleize strings
const titleize = function(str) {
    var profParts = $.trim(str).split(" ");
    var prof = [];
    for (var j = 0; j < profParts.length; j++) {
        prof.push(profParts[j][0].toUpperCase() + profParts[j].substr(1).toLowerCase());
    }
    return prof.join(" ");
}

//function to list professors when there are <= 15
const listProfessors = function() {
  var outerDiv = $('<div>');
  outerDiv.attr('id', 'divList');
  var listOfProfessors = $('<ul>');
  listOfProfessors.addClass('professorList');
  var avgButton = $('<button>Average professor</button>');
  avgButton.click(function(){
    addToCourseCart('average');
    addRemoveButton();
  });
  listOfProfessors.append($('<li>').append(avgButton));
  for (var i = 0; i < COURSE_DATA.instructors.length; i++) {
    const orig_prof = COURSE_DATA.instructors[i];
    const prof = titleize(orig_prof);
    const listItem = $('<li>');
    const button = $('<button>');
    button.click(
      function(){
        addToCourseCart(orig_prof);
        addRemoveButton();
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
  head.html('<span class="label">Filter by last name:</span>');
  var table = $('<table>');
  table.addClass("professorList");
  var tr = $('<tr>');
  var avgSection = $('<button>Average professor</button>');
  avgSection.click(function() {
      addToCourseCart('average');
      addRemoveButton();
  });
  avgList = $('<ul>');
  avgList.addClass('professorList');
  avgListitem = $('<li>');
  avgListitem.addClass('average');
  avgSection = avgList.append($(avgListitem).append(avgSection))
  head.prepend(avgSection);

  //create the grid of buttons of the alphabet
  for (var i = 1; i <= 26; i++) {
    const character = String.fromCharCode(i+64);
    var button = $('<button>');
    button.text(character);
    button.attr('data-value', character);
    var td = $('<td>');

    /*check to see if instructors exist with a last name starting with 'character'
    If so, leave the button clickable and functional; otherwise, gray it out.*/
    var containsCharAfterSpace = function(a, b) {
      return (b.split(' ').pop()[0] == character) || a;
    }

    if (!COURSE_DATA.instructors.reduce(containsCharAfterSpace, false)) {
      button.addClass('grayedOut');
    } else {
      button.click(function() {
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
          if (b.split(' ').pop()[0] == c) {
            var listItem = $('<li>');
            var button = $('<button>');
            button.attr('id', b.replace(/ /g, ''));
            button.click(
              function() {
                addToCourseCart(b);
                addRemoveButton();
              });
            button.append(titleize(b));
            listItem.append(button);
            a.append(listItem);
            return a;
          } else {
            return a;
          }
        }, $('<ul>').addClass('professorList'));
    $('#filteredProfs').append(listOfProfessors);

    $('.popover .selected').removeClass('selected');
    $('.popover').find('[data-value="' + c + '"]').addClass('selected');
  }
  popoverContent = $('<span>').append(head).append(table).append(filteredProfs);
}

//put the cart button under the scoreboxes
//fill the popover with professors/filtering interface
const addCartButton = function() {
  $('.courseCart').removeClass("d-none").find("i").addClass("fa-cart-plus").removeClass("fa-trash-alt");

  if (COURSE_DATA.instructors.length <= 15)
    listProfessors();
  else
    listAlphabet(null);
}

//remove the addCart button and replace it
//with a remove from cart option
const addRemoveButton = function() {
    $('.courseCart').removeClass("d-none").find("i").addClass("fa-trash-alt").removeClass("fa-cart-plus");
    $('#popup').popover('hide');
}

//when a professor is selected, add the remove button and
//add the class to localStorage. If the user's browser cannot
//handle localStorage usage, alert them.
const addToCourseCart = function(instructor) {
  $('[data-original-title]').popover('hide');
  localStorage.setItem(title,
    JSON.stringify(COURSE_DATA.instructor_data[instructor]));
}

const initializeCartButton = function(inCart) {
  if (inCart) {
    addRemoveButton();
  } else if (!inCart){
    addCartButton();
  }
}

$(document).ready(function() {
    $('.courseCart').click(function(e) {
        e.preventDefault();
        if ($('.courseCart').find('.fa').hasClass('fa-trash-alt')) {
            localStorage.removeItem(title);
            addCartButton();
        }
        else {
            $('#popup').popover({
                content: popoverContent,
                placement: 'bottom',
                html: true,
                animation: false
            }).popover('show');
            if (COURSE_DATA.instructors.length <= 15)
                listProfessors();
            else
                listAlphabet(null);
        }
    });
    $('html').on('click', function(e) {
        if (typeof $(e.target).attr("data-original-title") == 'undefined' && !$(e.target).is('button') && !$(e.target).parents().is('.popover')) {
            $('[data-original-title]').popover('hide');
            $('[data-original-title]').popover('hide');
        }
    });
});
