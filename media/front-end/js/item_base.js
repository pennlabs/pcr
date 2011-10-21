(function() {
  window.toggle_course_row_all = function() {
    if ($("th div.fold-icon").hasClass("open")) {
      $("th div.fold-icon").removeClass("open");
      $("td div.fold-icon").removeClass("open");
      return $(".row_hidden").hide();
    } else {
      $("th div.fold-icon").addClass("open");
      $("td div.fold-icon").addClass("open");
      return $(".row_hidden").show();
    }
  };
  window.toggle_course_row = function(index) {
    $("#row_hidden_" + index).toggle();
    if ($("#row_display_" + index + " td div.fold-icon").hasClass("open")) {
      return $("#row_display_" + index + " td div.fold-icon").removeClass("open");
    } else {
      return $("#row_display_" + index + " td div.fold-icon").addClass("open");
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
    localStorage["pcr_choosecols"] = result.join();
    toggle_choose_cols();
    return set_cols(result);
  };
  window.cancel_choose_cols = function() {
    var cols, i, _ref;
    $("#choose-cols input[type=checkbox]").attr("checked", false);
    cols = localStorage["pcr_choosecols"].split(",");
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      $("#choose-cols input[name='" + cols[i] + "']").attr("checked", true);
    }
    return toggle_choose_cols();
  };
  window.set_viewmode = function(view_id) {
    if (("" + view_id) === "0") {
      $("a#view_average").addClass("selected");
      $("a#view_recent").removeClass("selected");
      $(".cell_average").show();
      $(".cell_recent").hide();
    } else {
      $("a#view_average").removeClass("selected");
      $("a#view_recent").addClass("selected");
      $(".cell_average").hide();
      $(".cell_recent").show();
    }
    return localStorage["pcr_viewmode"] = view_id;
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
  /*
  DOCUMENT READY
  */
  $(document).ready(function() {
    var cols, i, _ref, _results;
    initSearchbox("../");
    $("#course-table").tablesorter({
      sortList: [[1, 0]],
      headers: {
        0: {
          sorter: false
        }
      }
    }).bind("sortStart", function() {
      return start_sort_rows();
    }).bind("sortEnd", function() {
      return end_sort_rows();
    });
    /* localStorage setup view mode */
    if (!(localStorage["pcr_viewmode"] != null)) {
      localStorage["pcr_viewmode"] = "0";
    }
    set_viewmode(localStorage["pcr_viewmode"]);
    /* localStorage setup choose columns */
    cols = (localStorage["pcr_choosecols"] != null) ? localStorage["pcr_choosecols"].split(",") : localStorage["pcr_choosecols"] = ["rCourseQuality", "rInstructorQuality", "rDifficulty"];
    set_cols(cols);
    _results = [];
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      _results.push($("#choose-cols input[name='" + cols[i] + "']").attr("checked", true));
    }
    return _results;
  });
}).call(this);
