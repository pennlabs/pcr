$(document).ready(function() {
    $("#search input[type='text']").selectize({
        labelField: 'title',
        searchField: ['title', 'keywords'],
        valueField: 'url',
        create: false,
        options: [],
        optgroups: [
            {"value": "Departments", "label": "Departments"},
            {"value": "Courses", "label": "Courses"},
            {"value": "Instructors", "label": "Instructors"},
        ],
        maxOptions: 10,
        optgroupField: 'category',
        render: {
            optgroup_header: function(data, esc) {
                return "<div class='optgroup-header'>" + esc(data.label) + "</div>";
            },
            option: function(item, esc) {
                return "<div>" + esc(item.title) + " <span class='sub'>"  + esc(item.desc) + "</span></div>";
            }
        },
        load: function(query, callback) {
            if (!query.length) {
                return callback();
            }
            $.getJSON("/autocomplete_data.json/" + query.toLowerCase() + ".json", function(data) {
                var out = data.courses.concat(data.departments).concat(data.instructors);
                callback(out);
            });
        },
        onItemAdd: function(value) {
            window.location.href = "/" + value;
            if ($("#loading").length) {
                $("#loading").show();
                $("#search .selectize-control").hide();
            }
            else {
                this.clear();
                this.disable();
            }
        }
    });
});
