###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#search-loading").hide()
    $("#search-container").fadeIn(1000, () ->
      $("#searchbox").focus()
    )
    alert("data loaded")
  $("#searchbox").keypress( () ->
    if $("#searchbox").val().length == 2
      init_search_box("", callback, $("#searchbox").val())
  )
  $("#search-loading").hide()
  $("#search-container").show()
