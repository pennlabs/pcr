window.autocomplete_open = ()->

$.widget "custom.autocomplete", $.ui.autocomplete, _renderMenu: (ul, items) ->
  self = this
  currentCategory = ""
  $.each items, (index, item) ->
    unless item.category == currentCategory
      ul.append "<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>"
      currentCategory = item.category
    self._renderItem(ul, item)

window.initSearchbox  = () ->
  $.getJSON "http://pennapps.com/pcrsite-nop/media/front-end/js/testdata.json",(data) ->
    $("#searchbox").autocomplete(
      source: data.items
      delay: 0
      minLength: 0
      
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