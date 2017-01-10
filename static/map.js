var get_bounds = function(galaxy) {
    var xmin = Infinity, xmax = -Infinity,
        ymin = Infinity, ymax = -Infinity;

    for (var sid in galaxy) {
        var system = galaxy[sid];
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
    $("#map .preload").append($("<p>").text("Loading map data..."));
    $.getJSON( "map/data.json", data => {
        var galaxy = data["systems"];
        var systems = Object.values(galaxy);
        var jumps = [].concat
            .apply([], Object.keys(galaxy)
                .map(src => galaxy[src]["gates"]
                    .map(dst => [parseInt(src), dst])))
            .filter(pair => pair[0] < pair[1]);

        var [xmin, ymin, xspan, yspan] = get_bounds(galaxy);
        var scale = 1000;
        var radius = scale / 2;

        var projx = x =>  ((x - xmin) / xspan - 0.5) * (scale * 0.99);
        var projy = y => -((y - ymin) / yspan - 0.5) * (scale * 0.99);

        $("#container > div").addClass("map-1");
        $("main").addClass("map-2");
        $("#map").addClass("map-3");
        $("#map .preload").remove();
        $("#map .controls").show();

        var svg = d3.select("#map").append("svg")
            .attr("viewBox", (-radius) + " " + (-radius) +
                  " " + scale + " " + scale);
        var stars = svg.append("g");

        stars.selectAll("line")
            .data(jumps)
            .enter()
            .append("line")
            .attr("x1", d => projx(galaxy[d[0]]["coords"][0]))
            .attr("y1", d => projy(galaxy[d[0]]["coords"][2]))
            .attr("x2", d => projx(galaxy[d[1]]["coords"][0]))
            .attr("y2", d => projy(galaxy[d[1]]["coords"][2]))
            .attr("class", "jump")
            .style("stroke-width", 1);

        stars.selectAll("circle")
            .data(systems)
            .enter()
            .append("circle")
            .attr("cx", d => projx(d["coords"][0]))
            .attr("cy", d => projy(d["coords"][2]))
            .attr("r", 2)
            .attr("class", d => {
                var sec = d["security"];
                var klass = sec <= 0.0 ? "null" :
                    Number(Math.max(sec, 0.1)).toFixed(1).replace(".", "_");
                return "system sec-" + klass;
            });

        var lastk = 1;
        var zoom = d3.zoom()
            .extent([[-radius, -radius], [radius, radius]])
            .scaleExtent([1, 63])
            .on("zoom", () => {
                var trans = d3.event.transform;
                var clamp = radius * (trans.k - 1);
                trans.x = Math.max(Math.min(trans.x, clamp), -clamp);
                trans.y = Math.max(Math.min(trans.y, clamp), -clamp);
                stars.attr("transform", trans);
                $("#map-scale").val(Math.log2(trans.k + 1));

                if (Math.abs((trans.k - lastk) / lastk) > 0.1) {
                    stars.selectAll("circle")
                        .attr("r", 6 / (trans.k + 2));
                    stars.selectAll("line")
                        .style("stroke-width", 2 / (trans.k + 1));
                    lastk = trans.k;
                }
            });
        svg.call(zoom);

        $("#map-scale").on("input", e => {
            var k = Math.pow(2, e.target.value) - 1;
            zoom.scaleTo(svg, k);
        })

        $(window).resize(() => {
            svg.style("display", "none")
                .attr("width", $("#map").width())
                .attr("height", $("#map").height())
                .style("display", "");
        });
        $(window).resize();
    });
});
