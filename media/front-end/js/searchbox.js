// Generated by CoffeeScript 1.10.0

/*
  Logic for the auto-complete search-box, on the home-page and top-right of
  every page.  Uses the jQuery UI autocomplete plugin.
 */

(function() {
  var MAX_ITEMS, REGEXES_BY_PRIORITY, endsWith, find_autocomplete_matches, get_entries;

  MAX_ITEMS = {
    Courses: 4,
    Instructors: 3,
    Departments: 3
  };

  endsWith = function(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length !== -1);
  };

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
        var found, i, len, term, terms;
        if (endsWith(search_term, " ")) {
          return false;
        } else {
          terms = search_term.trim().split(' ');
          found = false;
          for (i = 0, len = terms.length; i < len; i++) {
            term = terms[i];
            found = found || RegExp("\\s" + term + "[a-z]*$", 'i').test(instructor.keywords);
          }
          return found;
        }
      }), (function(search_term, instructor) {
        var found, i, len, term, terms;
        terms = search_term.trim().split(' ');
        found = false;
        for (i = 0, len = terms.length; i < len; i++) {
          term = terms[i];
          found = found || RegExp("^" + term, 'i').test(instructor.keywords);
        }
        return found;
      }), (function(search_term, instructor) {
        var found, i, len, term, terms;
        terms = search_term.trim().split(' ');
        found = false;
        for (i = 0, len = terms.length; i < len; i++) {
          term = terms[i];
          found = found || RegExp("\\s" + term, 'i').test(instructor.keywords);
        }
        return found;
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

  find_autocomplete_matches = function(search_str, category, sorted_entries) {
    var entry, i, j, len, len1, match_test, max, max_entry, ref, results, tests_passed;
    results = [];
    max = 0;
    max_entry = null;
    for (i = 0, len = sorted_entries.length; i < len; i++) {
      entry = sorted_entries[i];
      tests_passed = 0;
      ref = REGEXES_BY_PRIORITY[category];
      for (j = 0, len1 = ref.length; j < len1; j++) {
        match_test = ref[j];
        if (match_test(search_str, entry)) {
          tests_passed += 1;
        }
      }
      if (tests_passed > 1 || (tests_passed === 1 && results.length < MAX_ITEMS[category])) {
        if (tests_passed > max) {
          max = tests_passed;
          max_entry = entry;
        }
        results.push({
          passed: tests_passed,
          entry: entry
        });
      }
    }
    results = results.sort(function(a, b) {
      return b.passed - a.passed;
    });
    return $.map(results.slice(0, MAX_ITEMS[category]), function(result) {
      return result.entry;
    });
  };

  get_entries = function(term, courses, instructors, departments) {
    courses = find_autocomplete_matches(term, 'Courses', courses);
    departments = find_autocomplete_matches(term, 'Departments', departments);
    if (courses.length === 0 && departments.length === 0) {
      MAX_ITEMS['Instructors'] = 6;
    } else {
      MAX_ITEMS['Instructors'] = 3;
    }
    instructors = find_autocomplete_matches(term, 'Instructors', instructors);
    return courses.concat(instructors).concat(departments);
  };

  $.widget("custom.autocomplete", $.ui.autocomplete, {
    _renderMenu: function(ul, items) {
      var current_category;
      current_category = "";
      return $.each(items, (function(_this) {
        return function(index, item) {
          var li;
          if (item.category !== current_category) {
            li = "<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>";
            ul.append(li);
            current_category = item.category;
          }
          return _this._renderItem(ul, item);
        };
      })(this));
    }
  });

  window.init_search_box = function(dir, callback, start, fp) {
    var appendTo, leading, sort_by_title;
    if (dir == null) {
      dir = "";
    }
    if (callback == null) {
      callback = null;
    }
    sort_by_title = function(first, second) {
      if (first.title > second.title) {
        return 1;
      } else {
        return -1;
      }
    };
    if (fp) {
      appendTo = ".results";
    } else {
      appendTo = "#results_top";
    }
    if (dir.charAt(dir.length - 1) === "/") {
      leading = "";
    } else {
      leading = "/";
    }
    return $.getJSON(dir + "autocomplete_data.json/" + start.toLowerCase() + ".json", function(data) {
      var courses, departments, instructors;
      instructors = data.instructors.sort(sort_by_title);
      courses = data.courses.sort(sort_by_title);
      departments = data.departments.sort(sort_by_title);
      $("#searchbox").autocomplete({
        appendTo: appendTo,
        delay: 0,
        minLength: 2,
        autoFocus: true,
        selectFirst: true,
        source: function(request, response) {
          return response(get_entries(request.term, courses, instructors, departments));
        },
        position: {
          my: "left top",
          at: "left bottom",
          collision: "none",
          of: ".search",
          offset: "0 20"
        },
        focus: function(event, ui) {
          var focused;
          event.preventDefault();
          $(".focused").removeClass('focused');
          focused = $("a.ui-state-hover")[0].parentElement;
          if (!fp) {
            return $(focused).addClass('focused');
          }
        },
        select: function(event, ui) {
          window.location = dir + ui.item.url;
          return false;
        },
        open: function(event, ui) {
          return $(".ui-autocomplete.ui-menu.ui-widget").width($("#searchbar").width());
        }
      }).data("autocomplete")._renderItem = function(ul, item) {
        if (!fp) {
          ul.addClass("result_small");
        } else {
          ul.addClass("result_large");
        }
        return $("<li></li>").data("item.autocomplete", item).append("<a>\n  <div class='ui-menu-item-category'>" + item.category + "</div>\n  <div class='ui-menu-item-title'>" + item.title + "</div>\n  <div class='ui-menu-item-desc'>" + item.desc + "</div>\n</a>").appendTo(ul).fadeIn(500);
      };
      $('.ui-menu-item:first').trigger('autocompletefocus');
      if (callback != null) {
        return callback();
      }
    });
  };

}).call(this);
