(function() {
  window.toggle_row = function(row_id) {
    return $("#row_hidden_" + row_id).toggle();
  };
  window.toggle_choose_cols = function() {
    return $("#choose-cols").toggle();
  };
}).call(this);
