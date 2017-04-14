###
DOCUMENT READY
###
$(document).ready ->
  callback = () ->
    $("#searchbox").autocomplete("enable")
    $("#loading-container").hide()
    $("#searchbox").autocomplete("search")

  $('#searchbox').on 'paste', (e) ->
    setTimeout ->
      $('#loading-container').show()
      return init_search_box('', callback, $(this).val()[0...2], true)
    , 10

  $("#searchbox").keypress( () -> setTimeout(() ->
    if $("#searchbox").val().length == 2
      $("#loading-container").show()
      init_search_box("", callback, $("#searchbox").val(), true)
    else if $("#searchbox").val().length < 2
      $("#searchbox").autocomplete("disable")
  , 10))
