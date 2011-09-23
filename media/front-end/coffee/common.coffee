window.toggle_row = (row_id) ->
  $("#row_hidden_#{row_id}").toggle()  
  
window.toggle_choose_cols = () ->
  $("#choose-cols").toggle()

window.submit_choose_cols = () ->
# TODO: more efficient method please???
  str = ""
  for i in [0..10]
    str +=
    if $("#choose-cols input[name='choosecols#{i}']")
    .attr('checked')=="checked"
    then 1 else 0
    
  localStorage["pcr_choosecols"] = str
  toggle_choose_cols()
  
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

  ### setup view mode ###
  if not localStorage["pcr_view"]?
    localStorage["pcr_view"] = "0"
  else
    toggle_view(localStorage["pcr_view"])
  
  ### setup choose columns ###
  if localStorage["pcr_choosecols"]?
    str = localStorage["pcr_choosecols"]
  
    for i in [0..10]
      $("#choose-cols input[name='choosecols#{i}']")
        .attr('checked', str.charAt(i)=="1")
  else
    for i in [0..2]
      $("#choose-cols input[name='choosecols#{i}']")
        .attr('checked', true)
    localStorage["pcr_choosecols"] = "11100000000"