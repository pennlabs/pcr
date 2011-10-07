(function() {
  window.autocomplete_open = function() {};
  $.widget("custom.autocomplete", $.ui.autocomplete, {
    _renderMenu: function(ul, items) {
      var currentCategory, self;
      self = this;
      currentCategory = "";
      return $.each(items, function(index, item) {
        if (item.category !== currentCategory) {
          ul.append("<li class='ui-menu-item ui-autocomplete-category'><p>" + item.category + "</p></li>");
          currentCategory = item.category;
        }
        return self._renderItem(ul, item);
      });
    }
  });
  $(function() {
    return $.getJSON("http://pennapps.com/pcrsite-nop/media/front-end/js/testdata.json", function(data) {
      return $("#searchbox").autocomplete({
        source: data.items,
        delay: 0,
        minLength: 0,
        select: function(event, ui) {
          return alert(ui.item.label);
        },
        open: function(event, ui) {
          return autocomplete_open();
        }
      }).data("autocomplete")._renderItem = function(ul, item) {
        return $("<li></li>").data("item.autocomplete", item).append("<a><span class='ui-menu-item-title'>" + item.title + "</span><br/><span class='ui-menu-item-desc'>" + item.desc + "</span></a>").appendTo(ul);
      };
    });
  });
}).call(this);
