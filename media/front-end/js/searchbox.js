(function() {
  /*
    Logic for the auto-complete search-box, on the home-page and top-right of
    every page.  Uses the jQuery UI autocomplete plugin.
  */
  var MAX_NUM_COURSES, MAX_NUM_DEPARTMENTS, MAX_NUM_INSTRUCTORS, REGEXES_BY_PRIORITY, find_autocomplete_matches;
  var __indexOf = Array.prototype.indexOf || function(item) {
    for (var i = 0, l = this.length; i < l; i++) {
      if (this[i] === item) return i;
    }
    return -1;
  }, __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  MAX_NUM_COURSES = 6;
  MAX_NUM_INSTRUCTORS = 4;
  MAX_NUM_DEPARTMENTS = 3;
  REGEXES_BY_PRIORITY = {
    Courses: [
      (function(search_term, course) {
        return RegExp("^" + search_term, 'i').test(course.title);
      }), (function(search_term, course) {
        return RegExp("\\s" + search_term, 'i').test(course.keywords);
      }), (function(search_term, course) {
        return RegExp(search_term, 'i').test(course.keywords);
      })
    ],
    Instructors: [
      (function(search_term, instructor) {
        return RegExp("\\s" + search_term + "$", 'i').test(instructor.keywords);
      }), (function(search_term, instructor) {
        return RegExp("^" + search_term, 'i').test(instructor.keywords);
      })
    ],
    Departments: [
      (function(search_term, department) {
        return RegExp("^" + search_term, 'i').test(department.title);
      }), (function(search_term, department) {
        return RegExp("^" + search_term, 'i').test(department.keywords);
      })
    ]
  };
  find_autocomplete_matches = function(search_str, category, sorted_entries, max) {
    var entry, match_test, results, _i, _j, _len, _len2, _ref;
    results = [];
    _ref = REGEXES_BY_PRIORITY[category];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      match_test = _ref[_i];
      for (_j = 0, _len2 = sorted_entries.length; _j < _len2; _j++) {
        entry = sorted_entries[_j];
        if (match_test(search_str, entry) && !(__indexOf.call(results, entry) >= 0)) {
          results.push(entry);
          if (results.length === max) {
            return results;
          }
        }
      }
    }
    return results;
  };
  $.widget("custom.autocomplete", $.ui.autocomplete, {
    _renderMenu: function(ul, items) {
      var current_category;
      current_category = "";
      return $.each(items, __bind(function(index, item) {
        if (item.category !== current_category) {
          ul.append("<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>");
          current_category = item.category;
        }
        return this._renderItem(ul, item);
      }, this));
    }
  });
  window.init_search_box = function(dir, callback, start) {
    var sort_by_title;
    if (dir == null) {
      dir = "";
    }
    if (callback == null) {
      callback = null;
    }
    if (start == null) {
      start = "";
    }
    sort_by_title = function(first, second) {
      if (first.title > second.title) {
        return 1;
      } else {
        return -1;
      }
    };
    return $.getJSON(dir + "autocomplete_data.json/" + start, function(data) {
      var courses, departments, instructors;
      instructors = data.instructors.sort(sort_by_title);
      courses = data.courses.sort(sort_by_title);
      departments = data.departments.sort(sort_by_title);
      $("#searchbox").autocomplete({
        delay: 0,
        minLength: 2,
        autoFocus: true,
        source: function(request, response) {
          var result;
          result = find_autocomplete_matches(request.term, 'Courses', courses, MAX_NUM_COURSES).concat(find_autocomplete_matches(request.term, 'Instructors', instructors, MAX_NUM_INSTRUCTORS)).concat(find_autocomplete_matches(request.term, 'Departments', departments, MAX_NUM_DEPARTMENTS));
          return response(result);
        },
        position: {
          my: "left top",
          at: "left bottom",
          collision: "none",
          of: "#searchbar",
          offset: "0 -1"
        },
        focus: function(event, ui) {
          return false;
        },
        select: function(event, ui) {
          window.location = dir + ui.item.url;
          return false;
        },
        open: function(event, ui) {
          return $(".ui-autocomplete.ui-menu.ui-widget").width($("#searchbar").width());
        }
      }).data("autocomplete")._renderItem = function(ul, item) {
        return $("<li></li>").data("item.autocomplete", item).append("<a>\n  <span class='ui-menu-item-title'>" + item.title + "</span><br />\n  <span class='ui-menu-item-desc'>" + item.desc + "</span>\n</a>").appendTo(ul);
      };
      if (callback != null) {
        return callback();
      }
    });
  };
}).call(this);
