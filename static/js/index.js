$(document).ready(function() {
    if ($.cookie("pcr_banner") !== "false") {
        $("#banner").show();
    }
    $("#banner .close").click(function(e) {
        e.preventDefault();
        $("#banner").slideUp();
        $.cookie("pcr_banner", "false");
    });
});
