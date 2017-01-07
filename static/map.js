$(function() {
    $("#map").html("<p>Loading map data...</p>");
    $.getJSON( "map/data.json", function(data) {
        $("#map").empty();
        var svg = d3.select("#map").append("svg")
            .attr("width", 1000)
            .attr("height", 1000);  // TODO: dynamic

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

        var width = xmax - xmin;
        var height = ymax - ymin;
        var scale = 1000;

        svg.attr("viewBox", "0 0 " + scale + " " + scale);

        svg.selectAll("circle")
            .data(Object.values(data["galaxy"]))
            .enter()
            .append("circle")
            .attr("cx", (d) => {
                var x = d["coords"][0];
                return (x - xmin) / width * scale;
            })
            .attr("cy", (d) => {
                var y = d["coords"][2];
                return (y - ymin) / height * scale;
            })
            .attr("r", 1)
            .attr("class", (d) => {
                var sec = d["security"];
                var klass = sec < 0.05 ? "null" :
                    Number(sec).toFixed(1).replace(".", "_");
                return "system sec-" + klass;
            });
    });
});
