(function() {
  window.toggle_row = function(row_id) {
    return $("#row_hidden_" + row_id).toggle();
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
        result.push($(boxes[i]).attr("name"));
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
    $("#course-table .col_class_").show();
    $("#course-table .col_professor").show();
    $("#course-table .col_semester").show();
    $("#course-table .td_hidden").show();
    _results = [];
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      _results.push($("#course-table .col_" + cols[i]).show());
    }
    return _results;
  };
  /*
  DOCUMENT READY
  */
  $(document).ready(function() {
    /* localStorage setup view mode */
    var cols, i, _ref;
    if (!(localStorage["pcr_viewmode"] != null)) {
      localStorage["pcr_viewmode"] = "0";
    } else {
      set_viewmode(localStorage["pcr_viewmode"]);
    }
    /* localStorage setup choose columns */
    cols = (localStorage["pcr_choosecols"] != null) ? localStorage["pcr_choosecols"].split(",") : localStorage["pcr_choosecols"] = "class,difficulty,instructor";
    for (i = 0, _ref = cols.length - 1; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
      $("#choose-cols input[name='" + cols[i] + "']").attr("checked", true);
    }
    return set_cols(cols);
  });
}).call(this);
