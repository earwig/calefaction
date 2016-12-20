$(function() {
    // Install logout auto-POST form:
    $("#logout").click(function() {
        $("<form>", {
            "action": this.href,
            "method": "post"
        }).appendTo($("body")).submit();
        return false;
    });
});
