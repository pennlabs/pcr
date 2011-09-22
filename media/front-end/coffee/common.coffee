window.toggle_row = (row_id) ->
  $("#row_hidden_#{row_id}").toggle()  
  
window.toggle_choose_cols = () ->
  $("#choose-cols").toggle()