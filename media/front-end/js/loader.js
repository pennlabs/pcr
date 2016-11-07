var listProfessors = function() {
  var list = "<div id='divList'><ul class='professorList'>";
  for (var i = 0; i < instructors.length; i++) {
    list += "<li><button id='" + instructors[i].split(" ").join("") + 
      "' onclick='addToCourseCart(instructors[" + i  +"]);'>" +
      instructors[i]  + "</button></li>";
  }
  list += "</ul></div>";
  $("#popup").attr("data-content",list);
}

var listAlphabet = function(num) {
  var table = '<p>Filter by Last Name:</p><table class="professorList"><tr>';
  for (var i = 1; i <= 26; i++) {
    var character = String.fromCharCode(i+64)
    table += '<td><button id="letter' + character + '">' +
              character + '</button></td>';
    if (!instructors.reduce(
          function(a,b){
            return new RegExp("(\\s" + character 
                + "[A-Z])").test(b) || a
          }, false)) {
      $("#letter" + character).addClass('grayedOut'); 
    } else {
      var command = "listAlphabet('" + character + "');";
      $("#letter" + character).attr("onclick", command);
    }
    if (i%6 == 0)
      table += '</tr><tr>';
  }
  table += '</tr></table><div id="filteredProfessors"></div>';
  $("#popup").attr("data-content", table);
  if (num) {
    $("#filteredProfessors").html(instructors.reduce(
          function(a,b){
            return new RegExp("(\\s" + num + "[A-Z])").test(b) ?  a + 
              "<li><button id='" + b.split(" ").join("") + 
              "' onclick='addToCourseCart(\""+b+"\");'>"+ b +
              "</button></li>" : a
          }, "<ul class='professorList'>") + "</ul>");
    $("div.arrow").css("top", "103px");
  }
}

var addCartButton = function() {
  $("#banner-score")[0].innerHTML = $("#banner-score")[0].innerHTML +
    "<span class='button courseCart'><small id='popup' data-html='true'" +
    " data-toggle='popover' data-placement='left' data-content=''" + 
    "title='Select Professor'><i class='fa fa-cart-plus' aria-hidden='true'></i>i" +
    "  Add to My Cart</small></span>";
  if (instructors.length <= 15)
    listProfessors();
  else
    listAlphabet(null);
  
  $("[data-toggle=popover]").popover();
  $("[data-toggle=popover]").popover('hide');
  $(".courseCart").click(function() {
    $("[data-toggle=popover]").popover();
    if (instructors.length <= 15)
      listProfessors();
    else 
      listAlphabet(null);
  });
  $('body').on('hidden.bs.popover', function (e) {
    $(e.target).data("bs.popover").inState = { click: false, hover: false, focus: false }
  });
  $('html').on('click', function(e) {
    if (typeof $(e.target).data('original-title') == 'undefined' &&
        !$(e.target).is('button')  && 
        !$(e.target).parents().is('.popover.in')) {
      $('[data-original-title]').popover('hide');
      $('[data-original-title]').popover();
      $('[data-original-title]').popover('hide');
    }
  });
}
var addRemoveButton = function() {
  $('.courseCart').remove();
  $('#banner-score')[0].innerHTML = $('#banner-score')[0].innerHTML +
    "<span class='button courseCart'>" +
    "<small id='remove'><i class='fa fa-trash-o'></i>" +
    " Remove from My Cart</small></span>";
  $('#remove').click(function(){
    $("#remove").remove();
    addCartButton();
    localStorage.removeItem(title);
  });
}
addToCourseCart = function(instructor) {
  $('[data-original-title]').popover('hide');
  if (typeof(Storage) !== "undefined") {
    localStorage.setItem(title, JSON.stringify(instructor_data[instructor]));
    addRemoveButton();
  } else {
    alert("Sorry! Your browser does not support this feature." +
        " Please try again with a different browser.");
  }
}