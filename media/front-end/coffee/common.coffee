window.show_section = (row_id) -> 
  row = $("#row_#{row_id}").toggle()
  $("#row_toggle_#{row_id}").html(
    if row.is(":visible") then "Hide" else "Expand")