###
  Logic for the auto-complete search-box, on the home-page and top-right of
  every page.  Uses the jQuery UI autocomplete plugin.
###


# Maximum number of items to show per type
MAX_ITEMS =
    Courses: 6
    Instructors: 3
    Departments: 3


endsWith = (str, suffix) ->
    str.indexOf suffix, str.length - suffix.length != -1

# Rules for prioritizing items
REGEXES_BY_PRIORITY =
  Courses: [
    ((search_term, course) ->
        RegExp("^#{search_term}", 'i').test(course.title)),
    ((search_term, course) ->
        RegExp("\\s#{search_term}", 'i').test(course.keywords)),
    ((search_term, course) ->
        RegExp(search_term, 'i').test(course.keywords))
  ],
  Instructors: [
    # if instructors = [Rebecca Stein, Steve Ballmer]
    # we want Stein to show up first when we type 'ste'
    # note, instructor.keywords is just the instruct name in lowercase

    # match last name
    ((search_term, instructor) ->
      # if it ends with a space, middle names will match the regex
      if endsWith search_term, " "
        false
      else
          RegExp("\\s#{search_term}[a-z]*$", 'i').test(instructor.keywords))

    # match first name
    ((search_term, instructor) ->
      RegExp("^#{search_term}", 'i').test(instructor.keywords))

    # match middle name
    ((search_term, instructor) ->
      RegExp("\\s#{search_term}", 'i').test(instructor.keywords))
  ],
  Departments: [
    ((search_term, department) ->
      RegExp("^#{search_term}", 'i').test(department.title))
    ((search_term, department) ->
      RegExp("^#{search_term}", 'i').test(department.keywords))
  ]


# Generate a list of interesting items to show for a given search term.
# @param user-entered search term
# @param type of items. Should be one of 'Courses', 'Instructors', or
#   'Departments', 'mixed'
# @param callback function array of items to show passed in
find_autocomplete_matches = (search_str, category, cb) ->
  
  $.ajax 'chrome/api/search/',
  {
    data:{
      result_type:category,
      count:5,
      q:search_str
    },
    success: (data) ->
      results = JSON.parse(data).result
      rv = []
     
      if results.courses
        # filter out duplicate semesters
        uniqueCourses = {}
        for course, _ in results.courses
          course.category = "course"
          uniqueCourses[course.value] ?= course 
        for _, val of uniqueCourses
          rv.push(val)
        

      if results.instructors
        for instructor, _ in results.instructors
          instructor.category = "instructor"
          instructor.name ?= ""
        rv = rv.concat(results.instructors)

      if results.departments 
        for dept, _ in results.departments
          dept.title = dept.value
          dept.category = "department"
          dept.name ?= ""
        rv = rv.concat(results.departments)

      cb(rv)
    error: (error) ->
      cb([]) 
  }

# Get a list of interesting entries for a given search term
# @param user-entered search term
# @param list of all courses
# @param list of all instructors
# @param list of all departments
# @return list of interesting entries
get_entries = (term, courses, instructors, departments) ->
  find_autocomplete_matches(term, 'Courses', courses)
  .concat(find_autocomplete_matches(term, 'Instructors', instructors))
  .concat(find_autocomplete_matches(term, 'Departments', departments))


# Inject the category header (ex. instructor) before first result of each
# category
$.widget "custom.autocomplete", $.ui.autocomplete, _renderMenu: (ul, items) ->
  current_category = ""
  $.each items, (index, item) =>
    unless item.category == current_category
      li = "<li class='ui-autocomplete-category'><p>#{item.category}</p></li>"
      ul.append(li)
      current_category = item.category
    @_renderItem(ul, item)


# Initialize searchbox
# @param base directory
window.init_search_box = (dir="", callback=null, start) ->

  # put the data in the right order (cis 120 before cis 500)
  sort_by_title = (first, second) ->
    if first.title > second.title then 1 else -1

  $("#searchbox").autocomplete(
    delay: 0
    minLength: 2
    autoFocus: true
    source: (request, response) ->
      # update the entries to show
      find_autocomplete_matches(request.term, 'mixed', (matches)->
        response(matches)   
      )
    position:
      my: "left top"
      at: "left bottom"
      collision: "none"
      of: "#searchbar"
      offset: "0 -1"
    focus: (event, ui) ->
      false
    select: (event, ui) ->
      # On click, go to page

      # The route for an instructor is /instructor/{num}
      # The path in the data is of the form /instructors/{num}-{name}
      window.location = (dir + '/' + ui.item.category + '/' +
        if ui.item.category != 'instructor' then ui.item.value 
        else parseInt(ui.item.path.split('/')[2])
        )
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
                 <span class='ui-menu-item-title'>#{item.value}</span><br />
                 <span class='ui-menu-item-desc'>#{item.name}</span>
               </a>""")
      .appendTo(ul)

