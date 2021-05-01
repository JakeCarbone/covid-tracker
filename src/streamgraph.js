// Imports
import * as d3 from "d3";

////////////////////////////////////////////////////////
//////////////////// Setup /////////////////////////////
////////////////////////////////////////////////////////

let margin = ({ top: 100, right: 40, bottom: 100, left: 40 });

let height = 500;

let palette = ["#73a2ab", "#bc586e", "#c79164", "#1c3c4a", "#dbbfc5", "#924f5d", "#cc7e72", "#172121", "#172121"];

let data = d3.csv('https://raw.githubusercontent.com/JakeCarbone/covid-tracker/master/data/gdp_percentile_data.csv');


// https://github.com/JakeCarbone/covid-tracker/blob/master/data/gdp_percentile_data.csv
////////////////////////////////////////////////////////
/////////////////////// Functions //////////////////////////
////////////////////////////////////////////////////////

// Hover functions
let hover = function(svg, path) {

  svg
      .on("mousemove", moved)
      .on("mouseenter", entered)
      .on("mouseleave", left);

  const line = svg.append("g")
       .attr("display", "none");

  line.append("g")
      .selectAll("line")
      .data(series)
      .join("line")
      .attr("class", "cursor-line")
      .attr("fill", "#fff")
      .attr("stroke-width", 0.5)
      .attr("x1", 10)
      .attr("y1", height - 20)
      .attr("x2", 10)
      .attr("y2", 10);

  line.append("text")
      .attr("class", "text-year")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("x", 0)
      .attr("y", 26)
      .attr("transform", "rotate(-90 20 20) translate(0, -20)");

  line.append("g")
      .selectAll("text")
      .data(series)
      .join("text")
      .attr("class", "text-genre")
      .attr("font-weight", "bold")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("x", 5)
      .attr("y", height - 43)
      .attr("transform", "rotate(-90 10 460)");

  line.append("g")
      .selectAll("text")
      .data(data)
      .join("text")
      .attr("class", "text-rating")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("x", 14)
      .attr("y", height - 36);

  function moved(event) {

    event.preventDefault();
    const pointer = d3.pointer(event, this);

    const xm = x.invert(pointer[0]);
    const ym = y.invert(pointer[1]);
    const genre = d3.select(event.target).attr("data-genre");

    line.attr("transform", `translate(${pointer[0]},0)`)
        .style("visibility", "inherit");

    line.select(".text-year")
      .text(parseInt(xm));

    line.selectAll(".text-rating")
      .text(d => d.pub_year === parseInt(xm) ? d[genre] + " reviews" : "");

    line.selectAll(".text-genre")
      .style("visibility", "hidden")
      .filter(d => d.key === genre)
      .style("visibility", "inherit")
      .attr("fill", d => d.key === genre ? color(d.key) : "#000")
      .text(genre);

    line.selectAll(".cursor-line")
      .attr("stroke", "fff0")
      .filter(d => d.key === genre)
      .attr("stroke", d => d.key === genre ? color(d.key) : "#fff0")

    path.attr("opacity", d => d.key === genre ? 1 : 0.2);

    console.log(genre);

    if (genre === null) {
      path.attr("opacity", 1);
      line.style("visibility", "hidden");
    }
  }

  function entered() {
    line.attr("display", null);
  }

  function left() {
    line.attr("display", "none");
  }
};

let filter_data = function (owid_data) {
  let owid_data_copy = [...owid_data];
  let new_array = [];

  let vaccines_started = false;
  for (let i = 0; i < owid_data_copy.length; i += 1) {
    let row = owid_data_copy[i];
    let v_number = parseInt(row['new_vaccinations_smoothed']);

    if (v_number >= 1) {
      vaccines_started = true;
    }

    if (vaccines_started) {
      new_array.push(row);
    }

  }

  return new_array;
};

/////////////////////////////////////////////////////////
//////////////////// Creating the figure ////////////////
/////////////////////////////////////////////////////////

let y = d3.scaleLinear()
  .domain([d3.min(series, d => d3.min(d, d => d[0])), d3.max(series, d => d3.max(d, d => d[1]))])
  .range([height - margin.bottom, margin.top]);

let x = d3.scaleLinear()
  .domain(d3.extent(data, d => d.date))
  .range([margin.left, width - margin.right]);

let area = d3.area()
  .x(d => x(d.data.date))
  .y0(d => y(d[0]))
  .y1(d => y(d[1]))
  .curve(d3.curveNatural);


let series = d3.stack()
  .keys(['new_vaccinations_smoothed'])//(data.columns.slice(1,data.columns.length-1))
  .order(d3.stackOrderDescending)
  .offset(d3.stackOffsetSilhouette)
  (data);



let chart = function(){
  const svg = d3.select('#streamgraph').create("svg")
    .attr("viewBox", [0, 0, width, height]);

  const path = svg.append("g")
    .selectAll("path")
    .data(series[0])
    .join("path")
    // .attr("data-genre", d => d.key)
    .attr("fill", d => color(d.data.continent))
    .attr("d", area)
  
  svg.append("g")
    .call(xAxis);

  // svg.call(hover, path);

  return svg.node();
};

chart();