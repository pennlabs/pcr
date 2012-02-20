###
  Logic for the auto-complete search-box, on the home-page and top-right of
  every page.  Uses the jQuery UI autocomplete plugin.
###
MAX_NUM_COURSES = 6
MAX_NUM_INSTRUCTORS = 4
MAX_NUM_DEPARTMENTS = 3

REGEXES_BY_PRIORITY =
  Courses: [
    ((search_term, course) ->  RegExp("^#{search_term}", 'i').test(course.title)),
    ((search_term, course) -> RegExp("\\s#{search_term}", 'i').test(course.keywords)),
    ((search_term, course) -> RegExp(search_term, 'i').test(course.keywords))
  ],
  Instructors: [
    # if instructors = [Rebecca Stein, Steve Ballmer]
    # we want Stein to show up first when we type 'ste'
    ((search_term, instructor) ->
      RegExp("\\s#{search_term}$", 'i').test(instructor.keywords))
    ((search_term, instructor) ->
      RegExp("^#{search_term}", 'i').test(instructor.keywords))
  ],
  Departments: [
    ((search_term, department) ->
      RegExp("^#{search_term}", 'i').test(department.title))
    ((search_term, department) ->
      RegExp("^#{search_term}", 'i').test(department.keywords))
  ]

find_autocomplete_matches = (search_str, category, sorted_entries, max) ->
  # Regexes to match against, in order of interstingness
  results = []
  for match_test in REGEXES_BY_PRIORITY[category]
    for entry in sorted_entries
      # this regex matches this entry  and previous regex did not
      if match_test(search_str, entry) and not (entry in results)
        results.push(entry)
        return results if results.length is max
  return results

# Inject the category header (ex. instructor) before first result of each category 
$.widget "custom.autocomplete", $.ui.autocomplete, _renderMenu: (ul, items) ->
  current_category = ""
  $.each items, (index, item) =>
    unless item.category == current_category
      ul.append("<li class='ui-autocomplete-category'><p>#{item.category}</p></li>")
      current_category = item.category
    @_renderItem(ul, item)

# dir - base directory
window.init_search_box = (dir="", callback=null, start) ->

  # put the data in the right order (cis 120 before cis 500)
  sort_by_title = (first, second) ->
    if first.title > second.title then 1 else -1
  
  $.getJSON dir+"autocomplete_data.json/"+start, (data) ->
    instructors = data.instructors.sort(sort_by_title)
    courses = data.courses.sort(sort_by_title)
    departments = data.departments.sort(sort_by_title)

    $("#searchbox").autocomplete(
      delay: 0
      minLength: 2
      autoFocus: true
      source: (request, response) ->
        result = find_autocomplete_matches(request.term, 'Courses', courses, MAX_NUM_COURSES)
          .concat(find_autocomplete_matches(request.term, 'Instructors', instructors, MAX_NUM_INSTRUCTORS))
          .concat(find_autocomplete_matches(request.term, 'Departments', departments, MAX_NUM_DEPARTMENTS))
        response(result)
      position:
        my: "left top"
        at: "left bottom"
        collision: "none"
        of: "#searchbar"
        offset: "0 -1"
      focus: (event, ui) ->
        false
      select: (event, ui) ->
        window.location = dir+ui.item.url
        false
      open: (event, ui) ->
        $(".ui-autocomplete.ui-menu.ui-widget").width(
          $("#searchbar").width()
        )
    )
    .data("autocomplete")._renderItem = (ul, item) ->
      $("<li></li>")
      .data("item.autocomplete", item)
      .append("""<a>
                   <span class='ui-menu-item-title'>#{item.title}</span><br />
                   <span class='ui-menu-item-desc'>#{item.desc}</span>
                 </a>""")
      .appendTo(ul)
      
    callback() if callback? # did the auto_complete.json have a callback? call it.
