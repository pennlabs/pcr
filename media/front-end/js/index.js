(function() {
  /*
  DOCUMENT READY
  */  $(document).ready(function() {
    initSearchbox();
    return $("#searchbox").autocomplete("option", "autoFocus", true);
  });
}).call(this);
