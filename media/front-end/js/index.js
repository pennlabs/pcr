(function() {
  /*
  DOCUMENT READY
  */  $(document).ready(function() {
    var callback;
    callback = function() {
      return $("#searchbox").autocomplete("search");
    };
    $("#searchbox").keypress(function() {
      if ($("#searchbox").val().length === 2) {
        return init_search_box("", callback, $("#searchbox").val());
      }
    });
    $("#search-loading").hide();
    return $("#search-container").show();
  });
}).call(this);
