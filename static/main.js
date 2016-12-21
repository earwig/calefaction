var overlaps = function(needle, haystack) {
    return haystack.is(needle) || haystack.has(needle).length > 0;
};

$(function() {
    // Install logout auto-POST form:
    $("#logout").click(function() {
        $("<form>", {
            "action": this.href,
            "method": "post"
        }).appendTo($("body")).submit();
        return false;
    });

    // Toggle character options on click:
    var charopts = $("#character-options");
    charopts.hide();
    $("#character-portrait").click(function() {
        if (charopts.is(":visible")) {
            charopts.hide();
            $(document).off("mouseup.charopts");
        } else {
            charopts.show();
            $(document).on("mouseup.charopts", function(e) {
                if (!overlaps(e.target, charopts) &&
                        !overlaps(e.target, $("#character-portrait"))) {
                    charopts.hide();
                    $(document).off("mouseup.charopts");
                }
            });
        }
    }).css("cursor", "pointer");
});
