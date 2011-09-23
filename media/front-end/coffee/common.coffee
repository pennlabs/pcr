window.toggle_row = (row_id) ->
  $("#row_hidden_#{row_id}").toggle()  
  
window.toggle_choose_cols = () ->
  $("#choose-cols").toggle()
  
# 0=average (default), 1=recent
window.toggle_view = (view_id) ->
  if "#{view_id}" == "0"
    $("a#view_average").addClass("disabled")
    $("a#view_recent").removeClass("disabled")
  else
    $("a#view_average").removeClass("disabled")
    $("a#view_recent").addClass("disabled")
  localStorage["pcr_view"] = view_id
  
###
DOCUMENT READY
###
$(document).ready ->
  if not localStorage["pcr_view"]?
    localStorage["pcr_view"] = "0"
  else
    toggle_view(localStorage["pcr_view"])