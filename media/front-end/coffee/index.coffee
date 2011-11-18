###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#search-loading").hide()
    $("#search-container").fadeIn(1000, () ->
      $("#searchbox").focus()
    )
  init_search_box("", callback)
