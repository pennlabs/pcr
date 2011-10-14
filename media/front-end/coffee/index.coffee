###
DOCUMENT READY
###
$(document).ready ->  
  initSearchbox()
  $("#searchbox").autocomplete("option", "autoFocus", true)