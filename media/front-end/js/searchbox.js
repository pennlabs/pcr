(function() {
  var autocompleteFilter;
  autocompleteFilter = function(a, s, n) {
    var count, i, out, _i, _len;
    s = s.toLowerCase();
    out = [];
    count = 0;
    for (_i = 0, _len = a.length; _i < _len; _i++) {
      i = a[_i];
      if (i.keywords.indexOf(s) !== -1) {
        out.push(i);
        count++;
        if (count >= n) {
          return out;
        }
      }
    }
    return out;
  };
  $.widget("custom.autocomplete", $.ui.autocomplete, {
    _renderMenu: function(ul, items) {
      var currentCategory, self;
      self = this;
      currentCategory = "";
      return $.each(items, function(index, item) {
        if (item.category !== currentCategory) {
          ul.append("<li class='ui-autocomplete-category'><p>" + item.category + "</p></li>");
          currentCategory = item.category;
        }
        return self._renderItem(ul, item);
      });
    }
  });
  window.initSearchbox = function() {
    return $.getJSON("autocomplete_data.json", function(data) {
      return $("#searchbox").autocomplete({
        delay: 0,
        minLength: 1,
        source: function(request, response) {
          return response(autocompleteFilter(data.courses, request.term, 5).concat(autocompleteFilter(data.instructors, request.term, 5)));
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
          window.location = ui.item.url;
          return false;
        },
        open: function() {
          return $(".ui-autocomplete.ui-menu.ui-widget").width($("#searchbar").width());
        }
      }).data("autocomplete")._renderItem = function(ul, item) {
        return $("<li></li>").data("item.autocomplete", item).append("<a><span class='ui-menu-item-title'>" + item.title + "</span><br/><span class='ui-menu-item-desc'>" + item.desc + "</span></a>").appendTo(ul);
      };
    });
  };
}).call(this);
