var overlaps = function(needle, haystack) {
    return haystack.is(needle) || haystack.has(needle).length > 0;
};

$(function() {
    /* ============================= Universal ============================= */

    // Install logout auto-POST form:
    $("#logout").click(function() {
        $("<form>", {
            "action": this.href,
            "method": "post"
        }).appendTo($("body")).submit();
        return false;
    });

    // Allow user to dismiss flashes:
    $("#flashes > div").each(function() {
        $(this).prepend($("<a>", {
            addClass: "dismiss",
            href: "#"
        }).html("[&times;]").click(function() {
            $(this).parent().remove();
            return false;
        }));
    });

    // Toggle character options on click:
    var charopts = $("#character-options");
    charopts.hide();
    $("#character-portrait img").click(function() {
        if (charopts.is(":visible")) {
            charopts.hide();
            $(document).off("mouseup.charopts");
        } else {
            charopts.show();
            $(document).on("mouseup.charopts", function(e) {
                if (!overlaps(e.target, charopts) &&
                        !overlaps(e.target, $("#character-portrait img"))) {
                    charopts.hide();
                    $(document).off("mouseup.charopts");
                }
            });
        }
    }).css("cursor", "pointer").keypress(function (e) {
        if (e.which === 13)
            $(this).click();
    }).prop("title", "Options").prop("alt", "Options").prop("tabindex", 0);

    // Switch style immediately without reloading the page:
    $("#style-options form").submit(function() {
        var style = $(this).find('input[type="submit"]').data("style");
        var stylesheet = "/static/styles/" + style + ".css";
        $("#user-style").prop("href", stylesheet);
        $("#style-options .cur").removeClass("cur").find(":submit")
            .prop("disabled", false);
        $(this).addClass("cur").find(":submit").prop("disabled", true);
    });

    /* ============================== Modules ============================== */

    // Campaigns: enable form auto-submit on campaign change:
    $("#campaigns-select select").change(function() {
        this.form.submit();
    });
    $('#campaigns-select input[type="submit"]').hide();

    //Campaigns: selectively reveal operation summary details:
    $(".operation .killboard tr").mouseenter(function() {
        var div = $("<table>", {addClass: "killboard expanded"})
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
