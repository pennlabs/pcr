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
  
  $.cookie("pcr_choosecols", result.join(), {path: '/'})
  toggle_choose_cols()
  set_cols(result)

window.cancel_choose_cols = () ->
  $("#choose-cols input[type=checkbox]").attr("checked",false)
  
  cols = $.cookie("pcr_choosecols").split(",")
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
  $.cookie("pcr_viewmode", view_id, {path: '/'})

window.set_cols = (cols) ->
  # hide all cols
  $("#course-table th").hide()
  $("#course-table td").hide()
  # show default cols
  $("#course-table .col_icon").show()
  $("#course-table .col_code").show()
  $("#course-table .col_instructor").show()
  $("#course-table .col_semester").show()
  $("#course-table .col_section").show()
  $("#course-table .td_hidden").show()
  $("#course-table .sec_td_hidden").show()
  
  #course_col_count = 2
  #section_col_count = 2
  
  # loop cols
  for i in [0..(cols.length-1)]
    $("#course-table .col_#{cols[i]}").show()
    #course_col_count++
    #section_col_count++
    
  #$("td.td_hidden").attr("colspan", "#{course_col_count}")
  #$("td.sec_td_hidden").attr("colspan", "#{section_col_count}")
  

window.start_sort_rows = () ->
  $("#course-table .row_hidden").appendTo($("div#hidden"));

window.end_sort_rows = () ->
  $("#course-table .row_display").each(() ->
    index = $(this).attr("id").substr(12)
    $(this).after($("#row_hidden_#{index}"))
  )
  
###
DOCUMENT READY
###
$(document).ready ->
  initSearchbox("../")  
  $("#course-table").tablesorter({
    sortList: [[1,0]],  # starting sort order
    headers: {          # disable sort on col 0
      0: {
        sorter: false 
      }
    } 
  }).bind("sortStart",() -> 
    start_sort_rows()
  ).bind("sortEnd",() -> 
    end_sort_rows()
  )

  ### setup view mode ###
  if not $.cookie("pcr_viewmode")?
    $.cookie("pcr_viewmode", "0", {path: '/'})
  set_viewmode($.cookie("pcr_viewmode"))
  
  ### setup choose columns ###
  # check if key exists, else create default
  
  if not $.cookie("pcr_choosecols")?    
    $.cookie("pcr_choosecols", "rCourseQuality,rInstructorQuality,rDifficulty", {path: '/'})
  cols = $.cookie("pcr_choosecols").split(",")
  set_cols(cols)
  # loop cols
  for i in [0..(cols.length-1)]
    $("#choose-cols input[name='#{cols[i]}']").attr("checked", true)
    
  