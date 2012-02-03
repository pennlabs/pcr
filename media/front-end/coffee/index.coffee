###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#searchbox").autocomplete("search")
  $("#searchbox").keypress( () ->
    if $("#searchbox").val().length == 2
      init_search_box("", callback, $("#searchbox").val())
  )
  $("#search-loading").hide()
  $("#search-container").show()
