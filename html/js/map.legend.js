// d3.legend
// Copyright (c) 2015 S Benten
//
// Create legends for maps and graphs

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module with d3 as a dependency.
        define(['d3'], factory);
    } else if (typeof module === 'object' && module.exports) {
        // CommonJS
        module.exports = function (d3) {
            d3.legend = factory(d3);
            return d3.legend;
        }
    } else {
        // Browser global.
        root.d3.legend = factory(root.d3);
    }
}(this, function (d3) {

    // Public - contructs a new legend
    //
    // Returns a legend
    return function () {
        var svg = null,
            csv = d3_legend_csv,
            position = d3_legend_position,
            shape = d3_legend_shape,
            svgImg = d3_legend_svgimg,
            margin = d3_legend_margin,
            padding = d3_legend_padding,
            width = 0,
            height = 0;

        // Public: Constructor
        function legend(vis) {
            svg = getSVGNode(vis);

            var data = loadCSV();
        }

        // Public: sets or gets the csv data file for the legend
        //
        // v - String value of the csv location
        //
        // Returns value or legend
        legend.csv = function (v) {
            if (!arguments.length) return csv;
            csv = v == null ? v : d3.functor(v);

            return legend;
        }

        // Public: sets or gets the location for the legend
        //
        // v - Integer value of the legend location
        // Currently limited to the four corners defined below
        //
        //    +-+-+
        //    |0|1|
        //    +-+-+ 4
        //    |3|2|
        //    +-+-+
        //
        // Returns value or legend
        legend.position = function (v) {
            if (!arguments.length) return position;
            position = v == null ? v : d3.functor(v);

            return legend;
        }

        // Public: sets or gets the shape for the legend
        //
        // v - A d3.svg.symbol() with the type set, defauts to square
        // e.g. -  d3.svg.symbol().type("square")
        //
        // Returns value or legend
        legend.shape = function (v) {
            if (!arguments.length) return shape;
            shape = v == null ? v : d3.functor(v);

            return legend;
        }
        
        // Public: sets or gets the svg image for the legend
        //
        // v - An Svg Image loaded as an Xml Document (for styling purposes)
        //
        // Returns value or legend
        legend.svgImg = function (v) {
            if (!arguments.length) return svgImg;
            svgImg = v == null ? v : d3.functor(v);

            return legend;
        }

        // Public: sets or gets the margin for the legend
        //
        // v - Interger value for the margin applied to the outside 
        // of the legend
        //
        // Returns value or legend
        legend.margin = function (v) {
            if (!arguments.length) return margin;
            margin = v == null ? v : d3.functor(v);

            return legend;
        }

        // Public: sets or gets the padding for the legend
        //
        // v - Interger value for the padding applied to the inside 
        // of the legend
        //
        // Returns value or legend
        legend.padding = function (v) {
            if (!arguments.length) return padding;
            padding = v == null ? v : d3.functor(v);

            return legend;
        }
        
        // Private: Load the CSV data 
        //
        // Returns the loaded data
        function loadCSV() {

            d3.csv(csv(), function (error, rows) {
                if (error) console.error(error);

                setup(rows);
                return rows;
            });

        }

        // Private: Setup the legend from the data
        function setup(rows) {
            var s = d3.select(svg)
            var g = s.append("g");

            var rect = g.append("rect")
              .attr("class", "legendouter")

            // Get the largest width and height
            var max = getMaxSize(rows);

            space = margin() + padding()
            width = space + max[0];
            height = space  + max[1] * rows.length;

            var items = g.selectAll(".legend")
              .data(rows)
              .enter()
              .append("g")
              .attr("class", "legend")
              .attr("transform", function (d, i) { return "translate(0," + (i * max[1]) + ")"; });

            // Add the color swatch
            if (svgImg() != null) { 
              d3.xml(svgImg(), "image/svg+xml", function(xml) {  
                var img = document.importNode(xml.documentElement, true);
                items.append("g")
                  .attr("transform", function (d, i) { return "translate(" + max[0] + "," + max[1] + ")"; })
                  .attr("width", function(d) { return d.Width })
                  .attr("height", function(d) { return d.Height; })
                  .each( function(d) { return loadImage(this, img, d.Color, d.Width); } );  
                  
                finish(g, rect, items, max);
              });           
            } else {
              if (shape() != "circle")
                space += padding()
            
              switch (shape()){
                case "line":
                  createLine(items, max);
                  break;
                case "poly":
                  createRect(items, max);
                  break;
                default:
                  items.append("path")
                    .attr("d", d3.svg.symbol().type(shape()).size( function(d) { return d.Width; }  ))
                    .attr("transform", function (d, i) { return "translate(" + space + "," + max[1] + ")"; })
                    .attr("class", function (d) { return d.Color; });  
                  break;
              }  
              finish(g, rect, items, max);
            }
        }
        
        // Private: Create a set of lines
        function createLine(items, max) {
            var x1 = margin() + padding();
            var x2 = x1 + 20;
            var y = 10 + (max[1] / 2);
            
            return items.append("line")
                .attr("x1", x1)
                .attr("y1", y)
                .attr("x2", x2)
                .attr("y2", y)
                .attr("class", function (d) { return d.Color; });
        }
        
        // Private: Create a set of rectangles
        function createRect(items, max) {
            return items.append("rect")
                .attr("x", function (d) { return getRectX(d.Width, max[0]); })
                .attr("y", function (d) { return getRectY(d.Height, max[1]); })
                .attr("width", function (d) { return getRectWidth(d.Width); })
                .attr("height", function (d) { return getRectHeight(d.Height); })
                .attr("class", function (d) { return d.Color; });
        }

        // Private: Get the rectangle X position
        function getRectX(v, maxW) {
            return margin() + padding() + ((maxW - +v) / 2);
        }

        // Private: Get the rectangle Y position
        function getRectY(v, maxH) {
            return margin() + padding() + ((maxH - +v) / 2);
        }

        // Private: Get the rectangle width
        function getRectWidth(v) {
            return +v;
        }

        // Private: Get the rectangle height
        function getRectHeight(v) {
            return +v;
        }

        
        // Private: Complete rendering  - split to cope with async function calls
        function finish(g, rect, items, max){
            // Add the textual prompt
            var txt = items.append("text")
              .attr("x", function (d) { return getTextX(max[0]); })
              .attr("y", function (d) { return getTextY(max[1]); })
              .text(function (d) { return d.Text; });

            // Resize the background based on the contents
            var x, textWidth = 0;
            for (x in items[0]) {
                var bbox = items[0][x].getBBox();
                if (textWidth < bbox.width)
                    textWidth = bbox.width;
            }

            reposition(g, rect, max[1]);
            
        }

        // Private: Reposition legend background
        function reposition(obj, rect, maxH) {
            // get the holding svg node
            var s = svg.getBoundingClientRect();

            // get the legend grouping node 
            var g = obj[0][0].getBoundingClientRect();

            console.log(s);
            console.log(g);

            // default state
            var x = margin();
            var y = margin();

            switch (position()) {
                case 1:
                    // top right
                    x = s.width - g.width - (margin() * 2) - (padding() * 2);
                    break;
                case 2:
                    // bottom right
                    x = s.width - g.width - (margin() * 2) - (padding() * 2);
                    y = s.height - g.height - (margin() * 2) - (padding() * 2);
                    break;
                case 3:
                    // bottom left
                    y = s.height - g.height - (margin() * 2) - (padding() * 2);
                    break;
                case 4:
                    // external - adjust svg to size of contents
                    var w = g.width + (margin() * 4);
                    var h = g.height + (margin() * 4);

                    d3.select(svg)
                        .attr("width", (w > s.width) ? w : s.width)
                        .attr("height", (h > s.height) ? h : s.height);
            }

            // Add the legend background
            // There is no way of styling a grouping element in svg
            // so a rect will be used and carefully positioned
            rect.attr("x", x)
              .attr("y", y)
              .attr("width", g.width +  (margin() * 2 ))
              .attr("height", g.height + (margin() * 2));

            // move the container
            obj.attr("x", x)
              .attr("y", y)
              .attr("width", g.width + (margin() * 2))
              .attr("height", g.height + (margin() * 2))

            // move the legend items
            var items = obj.selectAll(".legend")
              .attr("transform", function (d, i) { return "translate(" + (x - margin()) + "," + (y + (i * maxH) - margin()) + ")"; });
        }     

        //Private: Load an Svg Image from Xml
        function loadImage(parent, child, css, size){
          var str = "{0}px".replace("{0}", size == "null" ? 0 : size);
          var n = parent.appendChild(child.cloneNode(true)); 
          d3.select(n)
            .attr("width", str)
            .attr("height", str)
            .attr("x", -size / 2)
            .attr("y", -size / 2)
            .attr("class", css);
        }       

        // Private: get the max width and height
        function getMaxSize(rows) {
            var max = [20, 20];
            var x = 0;
            for (x in rows) {
                if (max[0] < rows[x].Width)
                    max[0] = +rows[x].Width;
                if (max[1] < rows[x].Height)
                    max[1] = +rows[x].Height;
            }

            return max;
        }

        // Private: Get the text X position 
        function getTextX(maxW) {
            return margin() + (padding() * 2) + maxW;
        }

        //Private: Get the text Y poosition
        function getTextY(maxH) {
            return margin() + (padding() * 2) + (maxH / 2);
        }

        // Private: Get the SVG element
        function getSVGNode(el) {
            el = el.node()
            if (el.tagName.toLowerCase() === 'svg')
                return el

            return el.ownerSVGElement
        }

        //-Default methods--------------------------------

        function d3_legend_csv() { return ""; }

        function d3_legend_position() { return 1; }

        function d3_legend_shape() { return "square"; }
        
        function d3_legend_svgimg() { return null; }

        function d3_legend_margin() { return 5; }

        function d3_legend_padding() { return 5; }

        return legend
    };

}));