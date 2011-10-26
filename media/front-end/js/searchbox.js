(function() {
  var findAutoCompleteMatches, regexes_by_priority;
  var __indexOf = Array.prototype.indexOf || function(item) {
    for (var i = 0, l = this.length; i < l; i++) {
      if (this[i] === item) return i;
    }
    return -1;
  }, __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  regexes_by_priority = {
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
        return RegExp("(^|\\s)" + search_term, 'i').test(instructor.keywords);
      })
    ]
  };
  findAutoCompleteMatches = function(category, entries, search_str, max) {
    var entry, match_test, results, _i, _j, _len, _len2, _ref;
    results = [];
    _ref = regexes_by_priority[category];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      match_test = _ref[_i];
      for (_j = 0, _len2 = entries.length; _j < _len2; _j++) {
        entry = entries[_j];
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
      var currentCategory, self;
      self = this;
      currentCategory = "";
      return $.each(items, __bind(function(index, item) {
        if (item.category !== currentCategory) {
          ul.append("<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>");
          currentCategory = item.category;
        }
        return this._renderItem(ul, item);
      }, this));
    }
  });
  window.initSearchbox = function(dir, callback) {
    if (dir == null) {
      dir = "";
    }
    if (callback == null) {
      callback = null;
    }
    return $.getJSON(dir + "autocomplete_data.json", function(data) {
      $("#searchbox").autocomplete({
        delay: 0,
        minLength: 1,
        source: function(request, response) {
          var result;
          result = findAutoCompleteMatches('Courses', data.courses, request.term, 6).concat(findAutoCompleteMatches('Instructors', data.instructors, request.term, 4));
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
          $("#searchbox").attr("value", ui.item.title);
          return false;
        },
        select: function(event, ui) {
          window.location = dir + ui.item.url;
          return false;
        },
        open: function() {
          return $(".ui-autocomplete.ui-menu.ui-widget").width($("#searchbar").width());
        }
      }).data("autocomplete")._renderItem = function(ul, item) {
        return $("<li></li>").data("item.autocomplete", item).append("<a><span class='ui-menu-item-title'>" + item.title + "</span><br/><span class='ui-menu-item-desc'>" + item.desc + "</span></a>").appendTo(ul);
      };
      if (callback != null) {
        return callback();
      }
    });
  };
}).call(this);
