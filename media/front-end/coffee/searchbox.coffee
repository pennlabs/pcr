autocompleteFilter = (a, s, n) ->
  s = s.toLowerCase()
  out = []
  count = 0  
  for i in a
    if i.keywords.indexOf(s)!=-1
      out.push(i)
      count++
      if count>=n
        return out
  return out

$.widget "custom.autocomplete", $.ui.autocomplete, _renderMenu: (ul, items) ->
  self = this
  currentCategory = ""
  $.each items, (index, item) ->
    unless item.category == currentCategory
      ul.append "<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>"
      currentCategory = item.category
    self._renderItem(ul, item)

window.initSearchbox  = () ->
  $.getJSON("autocomplete_data.json", (data)->
    
    $("#searchbox").autocomplete(      
      delay: 0
      minLength: 1
      
      source: (request, response) ->
        response(
          autocompleteFilter(data.courses, request.term, 5)
          .concat(autocompleteFilter(data.instructors, request.term, 5))
        )
      
      position:
        my: "left top"
        at: "left bottom"
        collision: "none"
        of: "#searchbar"
        offset: "0 -1"
      
      focus: ( event, ui ) ->
        $("#searchbox").attr("value", ui.item.title)
        return false
      
      select: ( event, ui ) ->
        window.location = ui.item.url
        return false
      
      open: () ->
        $(".ui-autocomplete.ui-menu.ui-widget").width(
          $("#searchbar").width()
        )
    )
    .data("autocomplete")._renderItem = (ul, item) ->
      $("<li></li>")
      .data("item.autocomplete", item)
      .append("<a><span class='ui-menu-item-title'>" +
              item.title +
              "</span><br/><span class='ui-menu-item-desc'>" +
              item.desc +
              "</span></a>")
      .appendTo(ul)
  )
