(function() {
  var table;

  window.submit_choose_cols = function() {
    var boxes = $("#column-selector .dropdown-item");
    var result = [];
    boxes.each(function() {
      if ($(this).hasClass("selected")) {
        result.push($(this).attr("data-name"));
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
      table.columns().every(function() {
        var headerClass = $.grep(this.header().className.split(" "), function(v, i) {
          return v.indexOf("col_") === 0;
        }).join().substr(4);
        if (text_cols.indexOf(headerClass) !== -1) {
          num_cols.push(this.index());
        }
      });
      table.columns(num_cols).visible(true);
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
        displayLength: 5,
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

    $("#course-table tbody").on("click", "tr", function(e) {
        if ($("#course-details").length) {
            var data = table.row(this).data();
            var details = data[data.length - 1];
            $("#select-prof").hide();
            $("#course-details-wrapper").show().find("h3").text($.trim($(data[0]).text()));
            $("#course-details-data").html(details);
            var details_table = $("#course-details-data").find("table").attr("id", "course-details-table");
            details_table.find(".sec_row_hidden").show().appendTo($("#course-details-comments").find("table"));
            details_table.DataTable({
                autoWidth: false,
                displayLength: 5,
                dom: '<"toolbar">frtip',
                language: {
                    search: "",
                    paginate: {
                        previous: "<i class='fa fa-chevron-left'></i>",
                        next: "<i class='fa fa-chevron-right'></i>"
                    }
                }
            });
            $("#course-details-data").find("input[type=search]").addClass("form-control form-control-sm");
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
        item.attr("data-name", $.grep(this.header().className.split(" "), function(v, i) {
          return v.indexOf('col_') === 0;
        }).join().substr(4));
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
