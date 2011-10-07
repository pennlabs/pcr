window.autocomplete_open = ()->

$.widget "custom.autocomplete", $.ui.autocomplete, _renderMenu: (ul, items) ->
  self = this
  currentCategory = ""
  $.each items, (index, item) ->
    unless item.category == currentCategory
      ul.append "<li class='ui-menu-item ui-autocomplete-category'><p>" + item.category + "</p></li>"
      currentCategory = item.category
    self._renderItem(ul, item)

$ ->
  $.getJSON "http://pennapps.com/pcrsite-nop/media/front-end/js/testdata.json", (data) ->
    $("#searchbox").autocomplete(
      source: data.items
      delay: 0
      minLength: 0
      select: ( event, ui ) ->
        alert(ui.item.label)
      open: ( event, ui ) ->
        autocomplete_open()
    ).data("autocomplete")._renderItem = (ul, item) ->
      $("<li></li>")
      .data("item.autocomplete", item)
      .append("<a><span class='ui-menu-item-title'>" +
              item.title +
              "</span><br/><span class='ui-menu-item-desc'>" +
              item.desc +
              "</span></a>")
      .appendTo(ul)