(function() {
  window.course_rows;
  window.toggled_rows;
  window.toggle_course_row_all = function() {
    if ($("th div.fold-icon").hasClass("open")) {
      $("th div.fold-icon").removeClass("open");
      $("td div.fold-icon").removeClass("open");
      $(".row_hidden").hide();
      return window.toggled_rows = 0;
    } else {
      $("th div.fold-icon").addClass("open");
      $("td div.fold-icon").addClass("open");
      $(".row_hidden").show();
      return window.toggled_rows = window.course_rows;
    }
  };
  window.toggle_course_row = function(index) {
    $("#row_hidden_" + index).toggle();
    if ($("#row_display_" + index + " td div.fold-icon").hasClass("open")) {
      $("#row_display_" + index + " td div.fold-icon").removeClass("open");
      window.toggled_rows--;
    } else {
      $("#row_display_" + index + " td div.fold-icon").addClass("open");
      window.toggled_rows++;
    }
    if (window.toggled_rows === window.course_rows) {
      return $("th div.fold-icon").addClass("open");
    } else {
      return $("th div.fold-icon").removeClass("open");
    }
  };
  window.toggle_choose_cols = function() {
    return $("#choose-cols").toggle();
  };
  window.submit_choose_cols = function() {
    var boxes, i, result, _ref;
    boxes = $("#choose-cols input[type='checkbox']");
    result = [];
    for (i = 0, _ref = boxes.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      if ($(boxes[i]).attr("checked") != null) {
        result.push($(boxes[i]).attr("value"));
      }
    }
    $.cookie("pcr_choosecols", result.join(), {
      path: '/'
    });
    toggle_choose_cols();
    return set_cols(result);
  };
  window.cancel_choose_cols = function() {
    var cols, i, _ref;
    $("#choose-cols input[type=checkbox]").attr("checked", false);
    cols = $.cookie("pcr_choosecols").split(",");
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      $("#choose-cols input[name='" + cols[i] + "']").attr("checked", true);
    }
    return toggle_choose_cols();
  };
  window.set_viewmode = function(view_id) {
    if (("" + view_id) === "0") {
      $("#view_average").addClass("selected");
      $("#view_recent").removeClass("selected");
      $(".cell_average").show();
      $(".cell_recent").hide();
    } else {
      $("#view_average").removeClass("selected");
      $("#view_recent").addClass("selected");
      $(".cell_average").hide();
      $(".cell_recent").show();
    }
    $.cookie("pcr_viewmode", view_id, {
      path: '/'
    });
    return $('#course-table').trigger('update');
  };
  window.viewmode = function() {
    return $.cookie('pcr_viewmode');
  };
  window.set_cols = function(cols) {
    var i, _ref, _results;
    $("#course-table th").hide();
    $("#course-table td").hide();
    $("#course-table .col_icon").show();
    $("#course-table .col_code").show();
    $("#course-table .col_instructor").show();
    $("#course-table .col_semester").show();
    $("#course-table .col_section").show();
    $("#course-table .col_responses").show();
    $("#course-table .td_hidden").show();
    $("#course-table .sec_td_hidden").show();
    _results = [];
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      _results.push($("#course-table .col_" + cols[i]).show());
    }
    return _results;
  };
  window.start_sort_rows = function() {
    return $("#course-table .row_hidden").appendTo($("div#hidden"));
  };
  window.end_sort_rows = function() {
    return $("#course-table .row_display").each(function() {
      var index;
      index = $(this).attr("id").substr(12);
      return $(this).after($("#row_hidden_" + index));
    });
  };
  window.setup_tutorial_overlay = function() {
    $("#tut-viewmode").css("top", $("#settings-viewmode").offset().top - 230);
    return $("#tut-choosecols").css("top", $("#settings-other").offset().top - 230);
  };
  /*
  DOCUMENT READY
  */
  $(document).ready(function() {
    var cols, i, _ref;
    $('.sec_row_hidden').hide();
    window.toggle_course_row_all();
    window.toggle_course_row_all();
    window.toggled_rows = 0;
    window.course_rows = parseInt($("#course-table").attr("count"), 10);
    init_search_box("../");
    if (!($.cookie("pcr_viewmode") != null)) {
      $.cookie("pcr_viewmode", "0", {
        path: '/'
      });
    }
    set_viewmode($.cookie("pcr_viewmode"));
    $("#course-table").tablesorter({
      sortList: [[1, 0]],
      headers: {
        0: {
          sorter: false
        }
      },
      textExtraction: function(node) {
        var element;
        element = (function() {
          switch (node.children.length) {
            case 0:
              return node;
            case 1:
              return node.children[0];
            default:
              return node.children[viewmode()];
          }
        })();
        return element.innerHTML;
      }
    }).bind("sortStart", function() {
      return start_sort_rows();
    }).bind("sortEnd", function() {
      return end_sort_rows();
    });
    if (!($.cookie("pcr_choosecols") != null)) {
      $.cookie("pcr_choosecols", "name,rCourseQuality,rInstructorQuality,rDifficulty", {
        path: '/'
      });
    }
    cols = $.cookie("pcr_choosecols").split(",");
    set_cols(cols);
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      $("#choose-cols input[name='" + cols[i] + "']").attr("checked", true);
    }
    if ($("#course-table").attr("count") === "1") {
      toggle_course_row_all();
    }
    return window.setup_tutorial_overlay();
  });
}).call(this);
