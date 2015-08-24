from bbox import *
from viz import *

class outputVars:
    """Details and functions required to parse the html required for the d3 map"""
    
    def __init__(self, main, hasHeader, idField, extTip, hasLegend, allowZoom, legendPosition, chartType, ranges, labels):
        """Constructor"""
        self.mainLayer = main
        self.bboxes = bounds()
        self.projectionScript = ""
        self.outputLayers = []
        self.hasHeader = hasHeader
        self.idField = idField
        self.extTip = extTip
        self.hasLegend = hasLegend
        self.allowZoom = allowZoom
        self.selectedLegendPosition = legendPosition
        self.chartType = chartType
        self.vizRanges = ranges
        self.vizLabels = labels        
        
    def tipInUse(self):
        """Is there a tip or chart in one of the layers"""
        tip = False
        for o in self.outputLayers:            
            if o.hasTip == True or o.hasViz == True:
                tip = True
            
        return tip
    
    def vizInUse(self):
        """Is there a chart in one of the layers"""
        viz = False
        for o in self.outputLayers:            
            if o.hasViz == True:
                viz = True
            
        return viz
            
        
    def createHeader(self, title):
        """Creating the optional heading element"""
        template = u"<h1>{0}</h1>"
        
        if self.hasHeader == True:
            return template.format(title)
        else:
            return ""
        
    def createSvgPaths(self):
        """Create the Svg group and path elements required by the layers"""
        paths = []
        template = "    var vectors{index} = vectors.append(\"g\");\n    var vector{index} = vectors{index}.append(\"path\");\n"
        i = 0
        for o in self.outputLayers:
            path = template.format(
                index = i
            )
            paths.append(path)
            i += 1
    
        return "".join(paths)
    
    def createZoom(self):
        """Create the JavaScript function to zoom"""
        if self.allowZoom:
            return "    svg.call(d3.behavior.zoom()\n      .scaleExtent([1, 40])\n      .on(\"zoom\", onZoom));"
        else:
            return "" 
        
    def createTipFunction(self):
        """Create the Javascript function for tips"""
        
        template = """    //Define 'div' for tooltips
    var tip = d3.tip()
      .attr("class", "d3-tip")
      .direction("c"){0};
    vectors.call(tip);"""
        ext = """
      .ext("#extTip")"""
        
        if self.tipInUse() == True:
            if self.extTip == True:
                return template.format(ext)
            else:
                return template.format("")
        else:
            return ""
        
    def hideTip(self):
        """Conditionally add the hide tip call to the map container"""
        if self.tipInUse() == True:
            return """      .on("click", hideTip)"""
        else:
            return ""
    
    def createChartFunction(self, vizWidth, vizHeight):
        """Create the chart javascript"""
        
        value = ""
        
        if self.vizInUse() == True:            
            value = self.chartType.getJavaScript(self.mainLayer, self.vizRanges, self.vizLabels, vizWidth, vizHeight, self.extTip)

        return value
        
           
     
    def createTipHelpers(self):
        """Create the tip helper functions"""
        template = """    // Show a tool tip for the selected element
    function showTip(id) {
      var obj = _.findWhere(_data, {<%idfield%>: id.toString()});
      tip.html(info(obj))
        .show();

      <%chart%>  
      
      d3.event.stopPropagation();
    }
    
    // Get the tool tip data from the template
    function info(obj) {
      var template = document.getElementById("template").innerHTML;
      
      Object.keys(obj).forEach(function(key){
        template = template.replace("{" + key + "}", obj[key]);
      });
    
      return template;
    }
    
    // Hide the tooltip
    function hideTip() {
      tip.hide();
    }"""
    
        val = ""
        
        if self.tipInUse() == True:
            val = template.replace("<%idfield%>", self.idField)
            cobj = ""
            if self.vizInUse() == True:
                cobj = "chart(obj);"
            val = val.replace("<%chart%>", cobj)
                
        return val
     
    def createZoomFunction(self):
        """Create the Javascript zoom helper functions"""       
        
        template = """    // Zoom/pan 
    function onZoom() {
      <%hidetip%>

      vectors.attr("transform", "translate("
        + d3.event.translate
        + ")scale(" + d3.event.scale + ")");

<%vectorscaling%>
    }"""
        
        if self.allowZoom == True:
            template = template.replace("<%vectorscaling%>", self.createZoomScaling())
            
            if self.tipInUse() == True:
                return template.replace("<%hidetip%>", "hideTip();")
            else:
                return template.replace("<%hidetip%>", "")
        else:
            return ""
    
    def createQueueScript(self):
        """Create the javascript queue of json files"""
        queue = []
        template = "      .defer(d3.json, \"topo/{name}.json\")\n"
        i = 0
        for o in self.outputLayers:               
            path = template.format(
                name = o.name
            )
            queue.append(path)
            i += 1
            
        if self.tipInUse():
            queue.append("      .defer(d3.csv, \"data/info.csv\")")
    
        return "".join(queue)
    
    def createReadyParams(self):
        """Create the JavaScript ready function parameters"""
        params = []
        template = ", json{index}"
        i = 0
        for o in self.outputLayers:             
            param = template.format(
                index = i
            )
            params.append(param)
            i += 1
            
        if self.tipInUse():
            params.append(", data")
    
        return "".join(params)    
    
    def createPolygonObjects(self):
        """Create the Svg polygon objects"""
        scripts = []
        template = "      var object{index} = topojson.feature(json{index}, json{index}.objects.l{index});\n"
        i = 0
        for o in self.outputLayers:
            script = template.format(
                index = i
            )
            scripts.append(script)
            i += 1
    
        return "".join(scripts)
    
    def createMainObject(self):
        """Get the name of the main object"""
        output = ""
        template = "object{index}"
        i = 0
        for o in self.outputLayers:
            if o.isMain:
                output = template.format(index = i)
                break
            i += 1
            
        return output
                
    
    def createVectorFeatures(self):
        """Create the polygon vector features"""
        scripts = []
        template = """      vector{index} = vectors{index}.selectAll("path").data(object{index}.features);
      vector{index}.enter()\n"""
        static = """        .append("path")
        .attr("id", function (d) { return d.id; })
        .attr("d", path)
        .attr("class", function (d) { return d.properties.d3Css; })"""
        tip = """\n        .on("click", function (d) { return showTip(d.id); });\n\n"""
        
        i = 0
        for o in self.outputLayers:
            script = template.format(
                index = i
            )
            scripts.append(script)
            scripts.append(static)

            if o.hasTip == True or o.hasViz == True:
                scripts.append(tip)
            else:
                scripts.append(";\n\n")
                
            i += 1
    
        return "".join(scripts)
        
    def createDataStore(self):
        """Optionally store a copy of the info.csv in JavaScript"""    
        if self.tipInUse() == True:
            return "      _data = data;"
        else:
            return ""
    
    def createLegend(self):
        """Add a call to the JavaScript function to add a legend"""           
        if self.hasLegend:
            template = """      {e}
      var legend = d3.legend({s})
        .csv("data/legend.csv")
        .position({p})
        .shape(RECT);
      {s}.call(legend);"""

            ext = ""
            svg = "svg"
            pos = self.selectedLegendPosition
                  
            if self.selectedLegendPosition == 4:
                # external legend has to have a different hosting svg element
                ext = """var extLgnd = d3.select("#extLgnd")
        .append("svg");\n"""
                svg = "extLgnd"

            # format and return
            return template.format(
                e = ext,
                s = svg,
                p = pos
            )
                
        else:
            return "" 
    
    def createExtLegend(self):
        """Add a placeholder for the external legend"""
        if self.hasLegend == True and self.selectedLegendPosition == 4:
            return """  <div id="extLgnd"></div>"""
        else:
            return ""
        
    def createExtTip(self):
        """Add a placeholder for the external tip"""
        if self.tipInUse() == True and self.extTip == True:
            return """  <div id="extTip"></div>"""
        else:
            return ""        
        
    def createZoomScaling(self):
        """Create the JavaScript to re-scale the vectors"""
        template = "      vector{index}.style(\"stroke-width\", {width} / d3.event.scale);\n"
        scripts = []
        if self.allowZoom:
            i = 0
            for o in self.outputLayers:
                if o.strokeWidth > 0:
                    script = template.format(
                        index = i,
                        width = o.strokeWidth
                    )
                    scripts.append(script)
                i += 1
    
        return "".join(scripts)  
               
class outputLayer:
    """Details of layer details for the d3 map"""
    
    def __init__(self, objName, name, averageWidth, main, hasTip, hasViz):
        """Constructor"""
        self.objName = objName
        self.name = name
        self.isMain = main
        self.hasTip = hasTip
        self.hasViz = hasViz
        self.strokeWidth = averageWidth