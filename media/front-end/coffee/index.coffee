###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#searchbox").autocomplete("enable")
    $("#searchbox").autocomplete("search")
  $("#searchbox").keypress( () -> setTimeout(() ->
    if $("#searchbox").val().length == 2
      init_search_box("", callback, $("#searchbox").val())
    else if $("#searchbox").val().length < 2
      $("#searchbox").autocomplete("disable")
  , 0))
  $("#search-loading").hide()
  $("#search-container").show()
