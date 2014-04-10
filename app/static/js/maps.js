

var width = window.innerWidth,
    height = window.innerHeight;

var projection = d3.geo.mercator()
    .scale(120)
    .translate([width / 2, height / 2])
    .precision(.1);

var path = d3.geo.path()
    .projection(projection);

//var graticule = d3.geo.graticule();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

/*
svg.append("path")
    .datum(graticule)
    .attr("class", "graticule")
    .attr("d", path);
*/



d3.json("/static/world-50m.json", function(error, world) {
    svg.insert("path", ".graticule")
      .datum(topojson.feature(world, world.objects.land))
      .attr("class", "land")
      .attr("d", path);

    svg.insert("path", ".graticule")
      .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
      .attr("class", "boundary")
      .attr("d", path);
    

    var pathLine = d3.svg.line()
        .interpolate("cardinal")
        .x(function(d) { return projection([d.lon, d.lat])[0]; })
        .y(function(d) { return projection([d.lon, d.lat])[1]; });

    var d = [{lon:-74,lat:50,name:'ny'}]

    var coord = projection([-122.0574, 37.41919999999999]);
    svg
      .selectAll('circle')
      .data(locations)
      .enter()
      .append('circle')
      .each(function(loc,i) {
        var coord = projection([loc[0],loc[1]]);
        d3.select(this)
          .attr('cx', coord[0])
          .attr('cy', coord[1])
          .attr('r',4)
          .attr('fill','black')
      })

    svg
      .append('circle')
      .attr('cx',coord[0])
      .attr('cy',coord[1])
      .attr('r',3)
      .attr('fill','black')

});


function assign_locations(loc) {
  locations = loc
}





