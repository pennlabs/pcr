(function() {
  /*
  DOCUMENT READY
  */  $(document).ready(function() {
    var callback;
    callback = function() {
      $("#search-loading").hide();
      return $("#search-container").fadeIn(1000);
    };
    return initSearchbox("", callback);
  });
}).call(this);
