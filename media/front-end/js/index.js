(function() {
  /*
  DOCUMENT READY
  */  $(document).ready(function() {
    var callback;
    callback = function() {
      $("#search-loading").hide();
      $("#search-container").fadeIn(1000, function() {
        return $("#searchbox").focus();
      });
      return alert("data loaded");
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
