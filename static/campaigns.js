$(function() {
    // Enable form auto-submit on campaign change:
    $("#campaigns-select select").change(function() {
        this.form.submit();
    });
    $('#campaigns-select input[type="submit"]').hide();

    //Selectively reveal operation summary details:
    $(".operation:not(.detail) .killboard tr").mouseenter(function() {
        var div = $("<table>", {addClass: "board expanded"})
            .css($(this).position())
            .css("background-color", $(this).css("background-color"))
            .css("position", "fixed")
            .append($("<tr>").html($(this).html()))
            .mouseleave(function() { $(this).remove(); });
        div.find(".spacer").remove();
        $(this).closest(".summary").find(".expanded").remove();
        $(this).closest(".contents").prepend(div);
        div.css("width", Math.max(div.width(), $(this).width()));
        div.css("position", "");
        div.css("clip-path", "inset(0 0% 0 0)");
    });
    $(".operation .summary").mouseleave(function() {
        $(this).find(".expanded").remove();
    });
});
