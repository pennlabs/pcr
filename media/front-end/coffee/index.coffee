###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#searchbox").autocomplete("enable")
    $("#loading-container").hide()
    $("#searchbox").autocomplete("search")

  $("#searchbox").keypress( () -> setTimeout(() ->
    if $("#searchbox").val().length == 2
      $("#loading-container").show()
      init_search_box("", callback, $("#searchbox").val(), true)
    else if $("#searchbox").val().length < 2
      $("#searchbox").autocomplete("disable")
  , 10))
