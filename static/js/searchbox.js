$(document).ready(function() {
    $("#search input[type='text']").selectize({
        labelField: 'title',
        searchField: ['title', 'keywords'],
        valueField: 'url',
        create: false,
        maxItems: 1,
        options: [],
        optgroups: [
            {"value": "Departments", "label": "Departments"},
            {"value": "Courses", "label": "Courses"},
            {"value": "Instructors", "label": "Instructors"},
        ],
        score: function(search) {
            var score = this.getScoreFunction(search);
            return function(item) {
                var sc = score(item);
                if (sc > 0 && item.category == "Departments") {
                    sc += 100;
                }
                return sc;
            };
        },
        optgroupField: 'category',
        render: {
            optgroup_header: function(data, esc) {
                return "<div class='optgroup-header'>" + esc(data.label) + "</div>";
            },
            option: function(item, esc) {
                return "<div>" + esc(item.title) + " <span class='sub'>"  + esc(item.desc) + "</span></div>";
            }
        },
        preload: true,
        load: function(query, callback) {
            this.settings.load = null;
            $.getJSON("/autocomplete_data.json/.json", function(data) {
                const out = data.courses.concat(data.departments).concat(data.instructors);
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
                this.setTextboxValue(value);
                this.disable();
                $("#search button .fa.fa-search").removeClass("fa-search").addClass("fa-spinner fa-spin");
            }
        }
    });
    $("#search").submit(function(e) {
        e.preventDefault();
    });
});
