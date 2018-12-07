$(document).ready(function() {
    function cleanInstructorName(str) {
        return str.toLowerCase().trim().replace(/^(\w+) \w{0,2}\.? (\w+)$/, '$1 $2').replace(/\W/g, '');
    }

    $.get("/live/" + encodeURIComponent(title1), function(data) {
        if (!Object.keys(data.courses).length) {
            return;
        }
        $("#live").append($("<span class='badge badge-info' title='This course will be taught in " + data.term + ".' />").text(data.term));
        data.credits = data.credits.toFixed(1);
        $("#live").append($("<span class='badge badge-primary' title='This course is " + data.credits + " credit unit(s).' />").text(data.credits + " CU"));

        var open_instructors = {};

        Object.entries(data.courses).forEach(function(set) {
            var key = set[0];
            var value = set[1];
            if (!value.length) {
                return;
            }
            var num_available = value.length;
            var num_open = 0;
            for (var i = 0; i < value.length; i++) {
                if (!value[i].is_closed && !value[i].is_cancelled) {
                    num_open += 1;

                    for (var j = 0; j < value[i].instructors.length; j++) {
                        open_instructors[cleanInstructorName(value[i].instructors[j].name)] = true;
                    }
                }
            }
            var type = value[0].activity_description;
            var badge = $("<span class='badge " + (num_open > 0 ? "badge-success" : "badge-danger") + "' title='" + num_open + " out of " + num_available + " " + type.toLowerCase() + " sections are open for this course.' />").text(type);
            badge.append($("<span class='count' />").text(num_open + "/" + num_available));
            $("#live").append(badge);
        });

        var old_instructors = data.instructors.slice();
        data.instructors = data.instructors.map(cleanInstructorName);

        $("#course-table tbody .col_instructor").each(function() {
            var name = cleanInstructorName($(this).text());
            var idx = data.instructors.indexOf(name);
            if (idx !== -1) {
                data.instructors.splice(idx, 1);
                $(this).append("<i class='" + (open_instructors[name] ? "fa" : "far") + " fa-star' title='This instructor is teaching during " + data.term + ", and their section(s) are " + (open_instructors[name] ? "open" : "closed") + ".' />");
            }
        });

        if (data.instructors.length > 0) {
            var inst_list = [];
            old_instructors.forEach(function(item) {
                if (data.instructors.indexOf(cleanInstructorName(item)) !== -1) {
                    if (data.instructor_links[item]) {
                        inst_list.push("<a href='" + data.instructor_links[item] + "'>" + $("<div />").text(item).html() + "</a>");
                    }
                    else {
                        inst_list.push($("<div />").text(item).html());
                    }
                }
            });
            $("#live").append($("<div class='new-instructors' />").html("New Instructors: " + inst_list.join(", ")));
        }

        if ($.fn.dataTable.isDataTable($("#course-table"))) {
            $("#course-table").DataTable().rows().invalidate();
            $("#course-table").DataTable().draw();
        }
    });
});