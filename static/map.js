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

var get_sec_class = function(sec) {
    return "sec-" + (
        sec <= 0.0 ? "null" :
        Number(Math.max(sec, 0.1)).toFixed(1).replace(".", "_"));
}

var get_faction_class = function(factions, faction) {
    if (faction < 0)
        return "neutral";
    if (factions[faction] !== undefined)
        return "faction faction-" + S(factions[faction]["name"]).slugify();
}

$(function() {
    $("#map .preload").append($("<p>").text("Loading map data..."));
    $.getJSON( "map/data.json", data => {
        var galaxy = data["systems"];
        var factions = data["factions"];

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
        var field = svg.append("g");

        field.selectAll("line")
            .data(jumps)
            .enter()
            .append("line")
            .attr("x1", d => projx(galaxy[d[0]]["coords"][0]))
            .attr("y1", d => projy(galaxy[d[0]]["coords"][2]))
            .attr("x2", d => projx(galaxy[d[1]]["coords"][0]))
            .attr("y2", d => projy(galaxy[d[1]]["coords"][2]))
            .attr("class", "jump")
            .style("stroke-width", 1);

        field.selectAll("circle")
            .data(systems)
            .enter()
            .append("circle")
            .attr("cx", d => projx(d["coords"][0]))
            .attr("cy", d => projy(d["coords"][2]))
            .attr("r", 2);

        var stars = field.selectAll("circle");
        var jumps = field.selectAll("line");

        var lastk = 1;
        var zoom = d3.zoom()
            .extent([[-radius, -radius], [radius, radius]])
            .scaleExtent([1, 63])
            .on("zoom", () => {
                var trans = d3.event.transform;
                var clamp = radius * (trans.k - 1);
                trans.x = Math.max(Math.min(trans.x, clamp), -clamp);
                trans.y = Math.max(Math.min(trans.y, clamp), -clamp);
                field.attr("transform", trans);
                $("#map-scale").val(Math.log2(trans.k + 1));

                if (Math.abs((trans.k - lastk) / lastk) > 0.1) {
                    stars.attr("r", 6 / (trans.k + 2));
                    jumps.style("stroke-width", 2 / (trans.k + 1));
                    lastk = trans.k;
                }
            });
        svg.call(zoom);

        $("#map-scale").on("input", e => {
            var k = Math.pow(2, e.target.value) - 1;
            zoom.scaleTo(svg, k);
        });

        $('#map .controls input[name="color"]').change(function() {
            if (this.value == "sec") {
                stars.attr("class", d =>
                    "system " + get_sec_class(d["security"]));
            }
            else if (this.value == "faction") {
                stars.attr("class", d =>
                    "system " + get_faction_class(factions, d["faction"]));
            }
        });

        $("#map-color-sec").prop("checked", true).change();

        $(window).resize(() => {
            svg.style("display", "none")
                .attr("width", $("#map").width())
                .attr("height", $("#map").height())
                .style("display", "");
        });
        $(window).resize();
    });
});
