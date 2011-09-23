(function() {
  window.toggle_row = function(row_id) {
    return $("#row_hidden_" + row_id).toggle();
  };
  window.toggle_choose_cols = function() {
    return $("#choose-cols").toggle();
  };
  window.submit_choose_cols = function() {
    var i, str;
    str = "";
    for (i = 0; i <= 10; i++) {
      str += $("#choose-cols input[name='choosecols" + i + "']").attr('checked') === "checked" ? 1 : 0;
    }
    localStorage["pcr_choosecols"] = str;
    return toggle_choose_cols();
  };
  window.toggle_view = function(view_id) {
    if (("" + view_id) === "0") {
      $("a#view_average").addClass("disabled");
      $("a#view_recent").removeClass("disabled");
    } else {
      $("a#view_average").removeClass("disabled");
      $("a#view_recent").addClass("disabled");
    }
    return localStorage["pcr_view"] = view_id;
  };
  /*
  DOCUMENT READY
  */
  $(document).ready(function() {
    /* setup view mode */
    var i, str, _results;
    if (!(localStorage["pcr_view"] != null)) {
      localStorage["pcr_view"] = "0";
    } else {
      toggle_view(localStorage["pcr_view"]);
    }
    /* setup choose columns */
    if (localStorage["pcr_choosecols"] != null) {
      str = localStorage["pcr_choosecols"];
      _results = [];
      for (i = 0; i <= 10; i++) {
        _results.push($("#choose-cols input[name='choosecols" + i + "']").attr('checked', str.charAt(i) === "1"));
      }
      return _results;
    } else {
      for (i = 0; i <= 2; i++) {
        $("#choose-cols input[name='choosecols" + i + "']").attr('checked', true);
      }
      return localStorage["pcr_choosecols"] = "11100000000";
    }
  });
}).call(this);
