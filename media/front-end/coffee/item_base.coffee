window.course_rows
window.toggled_rows


window.toggle_course_row_all = () ->
  if $("th div.fold-icon").hasClass("open")
    $("th div.fold-icon").removeClass("open")
    $("td div.fold-icon").removeClass("open")
    $(".row_hidden").hide()
    window.toggled_rows = 0
  else
    $("th div.fold-icon").addClass("open")
    $("td div.fold-icon").addClass("open")
    $(".row_hidden").show()
    window.toggled_rows = window.course_rows


window.toggle_course_row = (index) ->
  $("#row_hidden_#{index}").toggle()
  if $("#row_display_#{index} td div.fold-icon").hasClass("open")
    $("#row_display_#{index} td div.fold-icon").removeClass("open")
    window.toggled_rows--
  else
    $("#row_display_#{index} td div.fold-icon").addClass("open")
    window.toggled_rows++
  
  if window.toggled_rows == window.course_rows
    $("th div.fold-icon").addClass("open")
  else
    $("th div.fold-icon").removeClass("open")


window.toggle_choose_cols = () ->
  $("#choose-cols").toggle()


window.toggle_choose_cols_all = () ->
  if($("#choose-cols input[type='checkbox'][name='all']").attr("checked"))
    $("#choose-cols input[type='checkbox']").attr("checked", true)
  else
    $("#choose-cols input[type='checkbox']").attr("checked", false)

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
    $("#view_average").addClass("selected")
    $("#view_recent").removeClass("selected")
    $(".cell_average").show()
    $(".cell_recent").hide()
  else
    $("#view_average").removeClass("selected")
    $("#view_recent").addClass("selected")
    $(".cell_average").hide()
    $(".cell_recent").show()
  $.cookie("pcr_viewmode", view_id, {path: '/'})
  $('#course-table').trigger('update')


window.viewmode = -> $.cookie('pcr_viewmode')


window.set_cols = (cols) ->
  $("#course-table th").hide()
  $("#course-table td").hide()

  $("#course-table .col_icon").show()
  $("#course-table .col_code").show()
  $("#course-table .col_instructor").show()
  $("#course-table .col_semester").show()
  $("#course-table .col_section").show()
  $("#course-table .col_responses").show()
  $("#course-table .td_hidden").show()
  $("#course-table .sec_td_hidden").show()

  for i in [0..(cols.length-1)]
    $("#course-table .col_#{cols[i]}").show()


window.start_sort_rows = () ->
  $("#course-table .row_hidden").appendTo($("div#hidden"))


window.end_sort_rows = () ->
  $("#course-table .row_display").each(() ->
    index = $(this).attr("id").substr(12)
    $(this).after($("#row_hidden_#{index}"))
  )


window.setup_tutorial_overlay = () ->
  $("#tut-viewmode").css("top", $("#settings-viewmode").offset().top-230);
  $("#tut-choosecols").css("top", $("#settings-other").offset().top+5);
  $("#tut-ratings").css("top", $("#banner-bg").offset().top+15);
  $("#tut-sort").css("top", $("#course-table").offset().top-30);
  $("#tut-row").css("top", $("#course-table").offset().top+50);


###
DOCUMENT READY
###
$(document).ready ->
  # graceful degradation without javascript: by default, everything is open
  # and javascript hides everything
  # 1. Hide 'comments'
  $('.sec_row_hidden').hide()
  # 2. Hide 'sections'
  window.toggle_course_row_all() 
  window.toggle_course_row_all()# hack - called twice due to init bug TODO - fix

  window.toggled_rows = 0
  window.course_rows = parseInt($("#course-table").attr("count"), 10)

  # init search box
  init_search_box("../")
  
  # setup view mode #
  if not $.cookie("pcr_viewmode")?
    $.cookie("pcr_viewmode", "0", {path: '/'})
  set_viewmode($.cookie("pcr_viewmode"))
  
  # init table sorter
  $("#course-table").tablesorter({
    sortList: [[1,0]],  # starting sort order
    headers: {          # disable sort on col 0
      0: {
        sorter: false
      }
    },
    textExtraction: (node) ->
      #sort by average or recent depending on user's preference
      element = switch node.children.length
        when 0 then node #course name, for example
        when 1 then node.children[0] #<a href...> in instructor
        else node.children[viewmode()]#recent/average filter
      return element.innerHTML
  }).bind("sortStart",() ->
    start_sort_rows()
  ).bind("sortEnd",() ->
    end_sort_rows()
  )
  
  # setup choose columns # 
  if not $.cookie("pcr_choosecols")?
    $.cookie("pcr_choosecols", "name,rCourseQuality,rInstructorQuality,rDifficulty", {path: '/'})
  cols = $.cookie("pcr_choosecols").split(",")
  set_cols(cols)

  for i in [0..(cols.length-1)]
    $("#choose-cols input[name='#{cols[i]}']").attr("checked", true)
    
  # auto-expand if there's only one item in course-table
  if $("#course-table").attr("count") == "1"
    toggle_course_row_all()
    
  window.setup_tutorial_overlay();
