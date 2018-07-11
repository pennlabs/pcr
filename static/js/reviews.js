(function() {
  var table;

  window.submit_choose_cols = function() {
    var boxes = $("#column-selector .dropdown-item");
    var result = [];
    boxes.each(function() {
      if ($(this).hasClass("selected")) {
        result.push($(this).attr("data-id"));
      }
    });
    $.cookie("pcr_choosecols", result.join(), {
      path: '/'
    });
    return set_cols(result);
  };

  window.set_cols = function(cols) {
      table.columns().visible(false);
      table.columns(0).visible(true);
      var num_cols = [];
      var text_cols = [];
      for (var i = 0; i < cols.length; i++) {
        if (isNaN(cols[i])) {
          text_cols.push(cols[i]);
        }
        else {
          num_cols.push(cols[i]);
        }
      }
      if (text_cols.length > 0) {
        $.cookie("pcr_choosecols", "1,2,3", {
          path: '/'
        });
        return window.set_cols([1, 2, 3]);
      }
      else {
        table.columns(num_cols).visible(true);
      }
  };

  window.set_viewmode = function(view_id) {
    if (("" + view_id) === "0") {
      $("#view_average").addClass("btn-primary").removeClass("btn-secondary");
      $("#view_recent").addClass("btn-secondary").removeClass("btn-primary");
      $(".cell_average").show();
      $(".cell_recent").hide();
    } else {
      $("#view_recent").addClass("btn-primary").removeClass("btn-secondary");
      $("#view_average").addClass("btn-secondary").removeClass("btn-primary");
      $(".cell_average").hide();
      $(".cell_recent").show();
    }
    $.cookie("pcr_viewmode", view_id, {
      path: '/'
    });
    return $('#course-table').trigger('update');
  };

  $(document).ready(function() {
    $('.sec_row_hidden').hide();

    if ($.cookie("pcr_viewmode") == null) {
      $.cookie("pcr_viewmode", "0", {
        path: '/'
      });
    }

    table = $("#course-table").removeClass("d-none").DataTable({
        columnDefs: [
            {
                targets: [-1],
                visible: false
            }
        ],
        autoWidth: false,
        dom: '<"toolbar">frtip',
        language: {
            search: "",
            paginate: {
                previous: "<i class='fa fa-chevron-left'></i>",
                next: "<i class='fa fa-chevron-right'></i>"
            }
        },
        drawCallback: function() {
            set_viewmode($.cookie("pcr_viewmode"));
        }
    });

    $("#course-table_filter input[type=search]").addClass("form-control form-control-sm");
    table.columns().visible(false);
    table.columns([0, 1, 2, 3, 4]).visible(true);

    $("#course-table_wrapper div.toolbar").append("<div class='btn-group mr-1'><button id='view_average' class='btn btn-sm btn-primary'>Average</button> <button id='view_recent' class='btn btn-secondary btn-sm'>Most Recent</button></div>");

    $("#view_average").click(function(e) {
      e.preventDefault();
      window.set_viewmode(0);
    });

    $("#view_recent").click(function(e) {
      e.preventDefault();
      window.set_viewmode(1);
    });

    set_viewmode($.cookie("pcr_viewmode"));
    set_cols($.cookie("pcr_choosecols").split(","));

    // create a div element for the button
    var btn_div = document.createElement("div");
    btn_div.setAttribute("class", "btn-group dropleft");
    $("#course-table_filter").prepend( btn_div );
    $("#course-table_wrapper div.toolbar").append("<button id='dropdownMenuButton' class='btn btn-primary btn-sm dropdown-toggle' data-toggle='dropdown'><i class='fa fa-plus'></i></button>");
    // create a div element for the drop down menu
    var div = $("<div id='column-selector' class='dropdown-menu' aria-labelledby='dropDownMenuButton' />");
    // create dropdown menu inside div
    table.columns().every(function() {
        var title = $(this.header()).text().trim();
        var item = $("<a class='dropdown-item' data-id='" + this.index() + "'>" + title + "</a>");
        if (title == "Instructor" || title == "Section") {
            return;
        }
        div.append(item);
        if (this.visible()) {
            item.addClass("selected");
        }
    });
    $("#course-table_wrapper div.toolbar").prepend(div);

    $('#column-selector .dropdown-item').click(function(e) {
        e.stopPropagation();
        $(this).toggleClass("selected");
        window.submit_choose_cols();
    });
  });

}).call(this);
