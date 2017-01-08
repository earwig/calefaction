var get_bounds = function(data) {
    var xmin = Infinity, xmax = -Infinity,
        ymin = Infinity, ymax = -Infinity;

    for (var sid in data["galaxy"]) {
        var system = data["galaxy"][sid];
        var x = system["coords"][0];
        var y = system["coords"][2];
        if (x < xmin) xmin = x;
        if (x > xmax) xmax = x;
        if (y < ymin) ymin = y;
        if (y > ymax) ymax = y;
    }

    var xspan = xmax - xmin;
    var yspan = ymax - ymin;

    return [xmin, ymin, xspan, yspan];
}

$(function() {
    $("#map").append($("<p>").text("Loading map data..."));
    $.getJSON( "map/data.json", data => {
        var [xmin, ymin, xspan, yspan] = get_bounds(data);
        var scale = 1000;

        $("#container > div").addClass("map-1");
        $("main").addClass("map-2");
        $("#map").empty().addClass("map-3");

        var svg = d3.select("#map").append("svg")
            .attr("viewBox", (-0.5 * scale) + " " + (-0.5 * scale) +
                  " " + scale + " " + scale);
        var stars = svg.append("g");

        stars.selectAll("circle")
            .data(Object.values(data["galaxy"]))
            .enter()
            .append("circle")
            .attr("cx", d => {
                var x = d["coords"][0];
                return ((x - xmin) / xspan - 0.5) * scale;
            })
            .attr("cy", d => {
                var y = d["coords"][2];
                return ((y - ymin) / yspan - 0.5) * scale;
            })
            .attr("r", 2)
            .attr("class", d => {
                var sec = d["security"];
                var klass = sec < 0.05 ? "null" :
                    Number(sec).toFixed(1).replace(".", "_");
                return "system sec-" + klass;
            });

        var lastk = 1;
        var zoom = d3.zoom()
            .scaleExtent([1, 50])
            .on("zoom", () => {
                var trans = d3.event.transform;
                var clamp = (scale / 2) * (trans.k - 1);
                trans.x = Math.max(Math.min(trans.x, clamp), -clamp);
                trans.y = Math.max(Math.min(trans.y, clamp), -clamp);
                stars.attr("transform", trans);
                if (trans.k != lastk) {
                    stars.selectAll("circle").attr("r", 6 / (trans.k + 2));
                    lastk = trans.k;
                }
            })
        svg.call(zoom);

        $(window).resize(() => {
            svg.style("display", "none")
                .attr("width", $("#map").width())
                .attr("height", $("#map").height() - 5)
                .style("display", "");
        });
        $(window).resize();
    });
});
