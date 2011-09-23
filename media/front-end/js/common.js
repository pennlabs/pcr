(function() {
  window.toggle_row = function(row_id) {
    return $("#row_hidden_" + row_id).toggle();
  };
  window.toggle_choose_cols = function() {
    return $("#choose-cols").toggle();
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
    if (!(localStorage["pcr_view"] != null)) {
      return localStorage["pcr_view"] = "0";
    } else {
      return toggle_view(localStorage["pcr_view"]);
    }
  });
}).call(this);
