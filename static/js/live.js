$(document).ready(function() {
    $.get("/live/" + encodeURIComponent(title1), function(data) {
        if (!Object.keys(data.courses).length) {
            return;
        }
        $("#live").append($("<span class='badge badge-primary' />").text(data.credits + " CU"));
        Object.entries(data.courses).forEach(function(set) {
            var key = set[0];
            var value = set[1];
            if (!value.length) {
                return;
            }
            var num_available = value.length;
            var num_open = 0;
            for (var i = 0; i < value.length; i++) {
                if (value[i].course_status == 'O') {
                    num_open += 1;
                }
            }
            var badge = $("<span class='badge " + (num_open > 0 ? "badge-success" : "badge-danger") + "' />").text(value[0].activity_description);
            badge.append($("<span class='count' />").text(num_open + "/" + num_available));
            $("#live").append(badge);
        });
    });
});
