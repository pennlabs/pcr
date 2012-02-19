(function() {
  /*
  DOCUMENT READY
  */  $(document).ready(function() {
    var callback;
    callback = function() {
      $("#searchbox").autocomplete("enable");
      $("#loading-container").hide();
      return $("#searchbox").autocomplete("search");
    };
    return $("#searchbox").keypress(function() {
      return setTimeout(function() {
        if ($("#searchbox").val().length === 2) {
          $("#loading-container").show();
          return init_search_box("", callback, $("#searchbox").val());
        } else if ($("#searchbox").val().length < 2) {
          return $("#searchbox").autocomplete("disable");
        }
      }, 0);
    });
  });
}).call(this);
