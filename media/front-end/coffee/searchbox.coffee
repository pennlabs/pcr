regexes_by_priority =
  Courses: [
    ((search_term, course) ->  RegExp("^#{search_term}", 'i').test(course.title)),
    ((search_term, course) -> RegExp("\\s#{search_term}", 'i').test(course.keywords)),
    ((search_term, course) -> RegExp(search_term, 'i').test(course.keywords))
  ],
  Instructors: [
    ((search_term, instructor) -> RegExp("\\s#{search_term}$", 'i').test(instructor.keywords)),
    ((search_term, instructor) -> RegExp(search_term, 'i').test(instructor.keywords))
  ]

findAutoCompleteMatches = (category, entries, search_str, max) ->
  #Regexes to match against, in order of interstingness
  #TODO - bigger (earlier) courses first
  results = []
  for match_test in regexes_by_priority[category]
    for entry in entries
      if match_test(search_str, entry) and not (entry in results)
        results.push(entry)
        return results if results.length is max
  return results

$.widget "custom.autocomplete", $.ui.autocomplete, _renderMenu: (ul, items) ->
  currentCategory = ""
  $.each items, (index, item) =>
    unless item.category == currentCategory
      ul.append "<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>"
      currentCategory = item.category
    @_renderItem(ul, item)

window.initSearchbox = ->
  $.getJSON("autocomplete_data.json", (data) ->
    console.log "Finally loaded the autocomplete data"
    $("#searchbox").autocomplete(
      delay: 0
      minLength: 1
      source: (request, response) ->
        result = findAutoCompleteMatches('Courses', data.courses, request.term, 5)
          .concat(findAutoCompleteMatches('Instructors', data.instructors, request.term, 5))
        response(result)
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
     ).data("autocomplete")._renderItem = (ul, item) ->
      $("<li></li>")
      .data("item.autocomplete", item)
      .append("<a><span class='ui-menu-item-title'>" +
              item.title +
              "</span><br/><span class='ui-menu-item-desc'>" +
              item.desc +
              "</span></a>")
      .appendTo(ul)
  )
