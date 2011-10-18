window.toggle_course_row_all = () ->
  if $("th div.fold-icon").hasClass("open")
    $("th div.fold-icon").removeClass("open")
    $("td div.fold-icon").removeClass("open")
    $(".row_hidden").hide()
  else
    $("th div.fold-icon").addClass("open")
    $("td div.fold-icon").addClass("open")
    $(".row_hidden").show()

window.toggle_course_row = (index) ->
  $("#row_hidden_#{index}").toggle()
  if $("#row_display_#{index} td div.fold-icon").hasClass("open")
    $("#row_display_#{index} td div.fold-icon").removeClass("open")
  else
    $("#row_display_#{index} td div.fold-icon").addClass("open")

window.toggle_choose_cols = () ->
  $("#choose-cols").toggle()

window.submit_choose_cols = () ->
  boxes = $("#choose-cols input[type='checkbox']")  
  result = []

  for i in [0..(boxes.length-1)]
    if $(boxes[i]).attr("checked")?
      result.push($(boxes[i]).attr("value"))
  
  localStorage["pcr_choosecols"] = result.join()
  toggle_choose_cols()
  set_cols(result)

window.cancel_choose_cols = () ->
  $("#choose-cols input[type=checkbox]").attr("checked",false)
  
  cols = localStorage["pcr_choosecols"].split(",")
  for i in [0..(cols.length-1)]
    $("#choose-cols input[name='#{cols[i]}']").attr("checked", true)
    
  toggle_choose_cols()
  
# 0=average (default), 1=recent
window.set_viewmode = (view_id) ->
  if "#{view_id}" == "0"
    $("a#view_average").addClass("selected")
    $("a#view_recent").removeClass("selected")
    $(".cell_average").show();
    $(".cell_recent").hide();
  else
    $("a#view_average").removeClass("selected")
    $("a#view_recent").addClass("selected")
    $(".cell_average").hide();
    $(".cell_recent").show();
  localStorage["pcr_viewmode"] = view_id

window.set_cols = (cols) ->
  # hide all cols
  $("#course-table th").hide()
  $("#course-table td").hide()
  # show default cols
  $("#course-table .col_icon").show()
  $("#course-table .col_course").show()
  $("#course-table .col_instructor").show()
  $("#course-table .col_semester").show()
  $("#course-table .col_section").show()
  $("#course-table .td_hidden").show()
  # loop cols
  for i in [0..(cols.length-1)]
    $("#course-table .col_#{cols[i]}").show()
  
###
DOCUMENT READY
###
$(document).ready ->
  initSearchbox("../")

  ### localStorage setup view mode ###
  if not localStorage["pcr_viewmode"]?
    localStorage["pcr_viewmode"] = "0"
  set_viewmode(localStorage["pcr_viewmode"])
  
  ### localStorage setup choose columns ###
  # check if localStorage key exists, else create default
  cols = if (localStorage["pcr_choosecols"]?)
  then localStorage["pcr_choosecols"].split(",")
  else localStorage["pcr_choosecols"] = ["rCourseQuality","rInstructorQuality","rDifficulty"]
  set_cols(cols)
  # loop cols
  for i in [0..(cols.length-1)]
    $("#choose-cols input[name='#{cols[i]}']").attr("checked", true)
    
  