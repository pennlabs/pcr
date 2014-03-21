###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#searchbox").autocomplete("enable")
    $("#loading-container").hide()
    $("#searchbox").autocomplete("search")
  $("#searchbox").keypress( () -> setTimeout(() ->
      init_search_box("", callback, $("#searchbox").val())
  , 0))
