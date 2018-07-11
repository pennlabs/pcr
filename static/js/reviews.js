(function() {
  $("#course-table").addClass("d-none");

  window.toggle_choose_cols = function() {
    return $("#choose-cols").toggle();
  };

  window.toggle_choose_cols_all = function() {
    if ($("#choose-cols input[type='checkbox'][name='all']").prop("checked")) {
      return $("#choose-cols input[type='checkbox']").prop("checked", true);
    } else {
      return $("#choose-cols input[type='checkbox']").prop("checked", false);
    }
  };

  window.submit_choose_cols = function() {
    var boxes, i, j, ref, result;
    boxes = $("#choose-cols input[type='checkbox']");
    result = [];
    for (i = j = 0, ref = boxes.length - 1; 0 <= ref ? j <= ref : j >= ref; i = 0 <= ref ? ++j : --j) {
      if ($(boxes[i]).prop("checked")) {
        result.push($(boxes[i]).attr("value"));
      }
    }
    $.cookie("pcr_choosecols", result.join(), {
      path: '/'
    });
    toggle_choose_cols();
    return set_cols(result);
  };

  window.cancel_choose_cols = function() {
    var cols, i, j, ref;
    $("#choose-cols input[type=checkbox]").prop("checked", false);
    cols = $.cookie("pcr_choosecols").split(",");
    for (i = j = 0, ref = cols.length - 1; 0 <= ref ? j <= ref : j >= ref; i = 0 <= ref ? ++j : --j) {
      $("#choose-cols input[name='" + cols[i] + "']").prop("checked", true);
    }
    return toggle_choose_cols();
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

  window.viewmode = function() {
    return $.cookie('pcr_viewmode');
  };

  window.set_cols = function(cols) {
    var i, j, ref, results;
    $("#course-table th").hide();
    $("#course-table td").hide();
    $("#course-table .col_icon").show();
    $("#course-table .col_code").show();
    $("#course-table .col_name").show();
    $("#course-table .col_instructor").show();
    $("#course-table .col_semester").show();
    $("#course-table .col_section").show();
    $("#course-table .col_responses").show();
    $("#course-table .td_hidden").show();
    $("#course-table .sec_td_hidden").show();
    results = [];
    for (i = j = 0, ref = cols.length - 1; 0 <= ref ? j <= ref : j >= ref; i = 0 <= ref ? ++j : --j) {
      results.push($("#course-table .col_" + cols[i]).show());
    }
    return results;
  };

  window.start_sort_rows = function() {
    return $("#course-table .row_hidden").appendTo($("div#hidden"));
  };

  window.end_sort_rows = function() {
    return $("#course-table .row_display").each(function() {
      var index;
      index = $(this).attr("id").substr(12);
      return $(this).after($("#row_hidden_" + index));
    });
  }; 

  $(document).ready(function() {
    $('.sec_row_hidden').hide();
    if ($.cookie("pcr_viewmode") == null) {
      $.cookie("pcr_viewmode", "0", {
        path: '/'
      });
    }

    const table = $("#course-table").removeClass("d-none").DataTable({
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
        var id = $(this).attr("data-id");
        var visible = table.column(id).visible();
        if (visible) {
            table.column(id).visible(false);
            $(this).removeClass("selected");
        }
        else {
            table.column(id).visible(true);
            $(this).addClass("selected");
        }
    });
  });

}).call(this);
