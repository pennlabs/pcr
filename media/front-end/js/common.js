(function() {
  window.show_section = function(row_id) {
    var row;
    row = $("#row_" + row_id).toggle();
    return $("#row_toggle_" + row_id).html(row.is(":visible") ? "Hide" : "Expand");
  };
}).call(this);
