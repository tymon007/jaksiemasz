$(document).ready(function () {
    $("[data-hide-pass-target]").on("click", function () {
        var attr = $("#" + $(this).attr("data-hide-pass-target")).attr("type");
        if (attr == "password") {
            $("#" + $(this).attr("data-hide-pass-target")).attr("type", "text");
        } else if (attr == "text") {
            $("#" + $(this).attr("data-hide-pass-target")).attr("type", "password");
        }
    })
});