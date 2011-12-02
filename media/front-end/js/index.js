(function() {
  /*
  DOCUMENT READY
  */  $(document).ready(function() {
    var callback;
    callback = function() {
      $("#search-loading").hide();
      return $("#search-container").fadeIn(1000, function() {
        return $("#searchbox").focus();
      });
    };
    return init_search_box("", callback);
  });
}).call(this);
