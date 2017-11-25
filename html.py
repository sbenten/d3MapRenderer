import codecs
import os

from models import model
from logger import log

class index(object):
    """Class for formatting the index html file for the map"""
    
    def __init__(self):
        """Format the index file with scripts for the viz"""
        self.__logger = log(self.__class__.__name__)
        self.model = None
        self.layersForOutput = []
        self.mainLayer = None
        
    def tipInUse(self):
        """Is there a tip or chart in one of the layers"""
        tip = False
        for o in self.layersForOutput:            
            if o.hasTip == True or o.hasViz == True:
                tip = True
            
        return tip
    
    def vizInUse(self):
        """Is there a chart in one of the layers"""
        viz = False
        for o in self.layersForOutput:            
            if o.hasViz == True:
                viz = True
            
        return viz
            
        
    def createHeader(self, title):
        """Creating the optional heading element"""
        template = u"<h1>{0}</h1>"
        
        if self.model.showHeader == True:
            return template.format(title)
        else:
            return ""
        
    def createSvgPaths(self, labels, selectedProjection):
        """Create the Svg group and path elements required by the layers"""
        paths = []
        template = "    var vectors{index} = vectors.append(\"g\");\n    var vector{index} = void 0;\n"
        i = 0

        for i, o in enumerate(self.layersForOutput):
            path = template.format( index = i )
            paths.append(path)
            paths.append(o.renderers[0].symbols[0].safeSvgNode(i, selectedProjection.safeCentroid))

        if self.model.showLabels == True:
            labelTemplate = """    var label{index} = void 0;"""
            for l in labels:
                if l.hasLabels() == True:
                    path = labelTemplate.format( index = l.index )
                    paths.append(path)
    
        return "".join(paths)
    
    def createZoom(self, selectedProjection):
        """Create the JavaScript function to zoom"""
        if self.model.panZoom:
            return selectedProjection.zoomBehaviourScript()
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
            if self.model.isExternalTip() == True:
                return template.format(ext)
            else:
                return template.format("")
        else:
            return ""
        
    def hideTip(self):
        """Conditionally add the hide tip call to the map container"""
        if self.tipInUse() == True:
            return """.on("click", hideTip)\n      """
        else:
            return ""
    
    def createChartFunction(self, vizWidth, vizHeight):
        """Create the chart javascript"""
        
        value = ""
        
        if self.vizInUse() == True:           
            value = self.model.selectedVizChart.getJavaScript(self.model.getMainLayer(), self.model.ranges, self.model.vizLabels, self.model.vizWidth, self.model.vizHeight, self.model.isExternalTip())

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
            val = template.replace("<%idfield%>", self.model.idField)
            cobj = ""
            if self.vizInUse() == True:
                cobj = "chart(obj);"
            val = val.replace("<%chart%>", cobj)
                
        return val

    def createSymbologyFunctions(self):
        """Create the necessary helper functions for symbology to display correctly"""
        scripts = []
        
        for o in self.layersForOutput:
            script = o.renderers[0].symbols[0].getAdditionalScripts()
            # Ensure items in the list are unique 
            if script != "" and script not in scripts:
                scripts.append(script)                
        
        return "".join(scripts)
     
    def createSafeCentroidFunction(self, selectedProjection):
        """Create the JavaScript centroid helper function"""       
     
        if self.model.panZoom == True and selectedProjection.safeCentroid == True:
            return """    function getSafeCentroid(d) {
      var centroid = path.centroid(d);
      var clip_test_path = d3.geo.path().projection(projection);
      var clipped =  typeof(clip_test_path({ type: "MultiPoint", coordinates: [centroid] })) == "undefined";
      return clipped ? [0, 0] : centroid; 
    }
"""

        else:
            return ""
        
     
    def createZoomFunction(self, selectedProjection, labels):
        """Create the Javascript zoom helper functions"""       
        labelSize = """    function labelSize(orig, scale){
      var size = orig / (Math.ceil(scale/2));
      return (size > 0) ? size : 1;
    }\n\n"""
        
        template = """<%labelsize%>
    // Zoom/pan 
    function onZoom() {
      <%hidetip%>
      <%vectorscaling%>
      <%labelscaling%>
    }"""
     
        if self.model.panZoom == True:

            if self.tipInUse() == True:
                template = template.replace("<%hidetip%>", "hideTip();")
            else:
                template =  template.replace("<%hidetip%>", "")
                
            ''' Zoom scaling script '''     
            v = []
            
            ''' Projection wide scaling script '''
            v.append(selectedProjection.zoomScalingScript())
            
            ''' Symbol specific scaling script '''
            for i, o in enumerate(self.layersForOutput):
                v.append(o.renderers[0].symbols[0].zoomScalingScript(i, selectedProjection.safeCentroid))
                
            template = template.replace("<%vectorscaling%>", "".join(v))
            
            ''' Label scaling '''
            if self.model.showLabels == True:
                                
                template = template.replace("<%labelsize%>", labelSize)
                
                l = []
                
                for label in labels:
                    if label.hasLabels() == True:
                        l.append(label.zoomLabelScript(selectedProjection.safeCentroid))                                       
                
                if len(l) > 0:     
                    template = template.replace("<%labelscaling%>", "".join(l))
                else:
                    template = template.replace("<%labelscaling%>", "")  
                       
            else:
                template = template.replace("<%labelsize%>", "")
                template = template.replace("<%labelscaling%>", "")
            
            return template
        else:
            return ""
    
    def createQueueScript(self):
        """Create the javascript queue of json files"""
        queue = []
        template = "      .defer(d3.json, \"json/{name}.json\")\n"
        
        for o in self.layersForOutput:               
            path = template.format(
                name = o.getSafeName()
            )
            queue.append(path)
            
        if self.tipInUse():
            queue.append("      .defer(d3.csv, \"data/info.csv\")")
    
        return "".join(queue)
    
    def createReadyParams(self):
        """Create the JavaScript ready function parameters"""
        params = []
        template = ", json{index}"

        for i, o in enumerate(self.layersForOutput):             
            param = template.format(
                index = i
            )
            params.append(param)
            
        if self.tipInUse():
            params.append(", data")
    
        return "".join(params)    
    
    def createMainObject(self):
        """Get the name of the main object"""
        output = ""
        template = "object{index}"
        i = 0
        for o in self.layersForOutput:
            if o.main:
                output = template.format(index = i)
                break
            i += 1
            
        return output
    
    def createLabelFeatures(self, selectedProjection, labels):
        """Create the label features"""
        scripts = []
        
        if self.model.showLabels == True:            
            for l in labels:
                if l.hasLabels() == True:
                    scripts.append(l.getLabelObjectScript(selectedProjection.safeCentroid))
        
        return "".join(scripts)
        
    def createDataStore(self):
        """Optionally store a copy of the info.csv in JavaScript"""    
        if self.tipInUse() == True:
            return "      _data = data;"
        else:
            return ""
    
    def createLegend(self):
        """Add a call to the JavaScript function to add a legend"""           
        if self.model.legend:
            template = """      {e}
      var legend = d3.legend({s})
        .csv("data/legend.csv")
        .position({p})
        .{f}("{a}");
      {s}.call(legend);"""

            func = "shape"
            arg = "square"
            
            # Find the main layer and check the first symbol to determine the correct JS function call
            m = self.model.getMainLayer()
            if m.renderers[0].symbols[0].hasImage() == True:
                func = "svgImg"
                head, tail = os.path.split(m.renderers[0].symbols[0].path)
                arg = "img/{0}".format(tail)
            else:
                arg = m.renderers[0].symbols[0].getShape()    
                
            ext = ""
            svg = "svg"
            pos = self.model.selectedLegendPosition
            
                  
            if self.model.selectedLegendPosition == 4:
                # external legend has to have a different hosting svg element
                ext = """var extLgnd = d3.select("#extLgnd")
        .append("svg");\n"""
                svg = "extLgnd"

            # format and return
            return template.format(
                e = ext,
                f = func,
                a = arg,
                s = svg,
                p = pos
            )
                
        else:
            return "" 
    
    def createExtLegend(self):
        """Add a placeholder for the external legend"""
        if self.model.legend == True and self.model.selectedLegendPosition == 4:
            return """  <div id="extLgnd"></div>"""
        else:
            return ""
        
    def createExtTip(self):
        """Add a placeholder for the external tip"""
        if self.tipInUse() == True and self.model.isExternalTip() == True:
            return """  <div id="extTip"></div>"""
        else:
            return ""    
                           
    def createVectorFeatures(self):
        """Create the polygon vector features"""
        
        scripts = []
        template = """      vector{index} = vectors{index}.selectAll("path").data(object{index}.features);
      vector{index}.enter()
        .append("path")\n"""
        main = """        .attr("id", function (d) {{ return d.properties.""" + self.model.idField + """; }})\n"""
        static = """        .attr("class", function (d) {{ return d.properties.d3Css; }})"""
        tip = """\n        .on("click", function (d) {{ return showTip(d.properties.""" + self.model.idField + """); }});\n\n"""
        
        for i, o in enumerate(self.layersForOutput):
            layerScript = []
            script = template.format(
                index = i
            )
            layerScript.append(script)
            if o.main == True:
                layerScript.append(main)
            layerScript.append("{0}")
            layerScript.append(static)

            if o.hasTip == True or o.hasViz == True:
                layerScript.append(tip)
            else:
                layerScript.append(";\n\n")

            scripts.append(o.renderers[0].symbols[0].toLayerScript( i, "".join(layerScript), self.model.selectedProjection.safeCentroid ) )     
    
        return "".join(scripts)
 
    def writeIndexFile(self, path, model, bound, labels):
        """Read and write the index html file"""
        self.model = model
        self.mainLayer = self.model.getMainLayer()
        self.layersForOutput = self.model.getLayersForOutput()
        
        f = codecs.open(path, "r", encoding="utf-8")        
        # Get the contents of the file
        html = f.read()
        f.close()
        
        # Can't use string format as it has a fit over css and javascript braces {}
        outHtml = u""
        outHtml = html.replace("<%title%>", self.model.title)
        outHtml = outHtml.replace("<%header%>", self.createHeader(self.model.title))
        outHtml = outHtml.replace("<%tooltiptemplate%>", self.model.selectedFormat.getPopupTemplate(self.model.selectedFields, self.vizInUse(), self.model.vizWidth, self.model.vizHeight))
        outHtml = outHtml.replace("<%externallegend%>", self.createExtLegend())
        outHtml = outHtml.replace("<%externaltip%>", self.createExtTip())
        outHtml = outHtml.replace("<%width%>", str(self.model.width))
        outHtml = outHtml.replace("<%height%>", str(self.model.height))
        outHtml = outHtml.replace("<%projection%>", self.model.selectedProjection.toScript(bound, self.model.width, self.model.height))
        outHtml = outHtml.replace("<%vectorpaths%>", self.createSvgPaths(labels, self.model.selectedProjection))
        outHtml = outHtml.replace("<%attachzoom%>", self.createZoom(self.model.selectedProjection))
        outHtml = outHtml.replace("<%hidetip%>", self.hideTip())
        outHtml = outHtml.replace("<%attachtip%>", self.createTipFunction())
        outHtml = outHtml.replace("<%queuefiles%>", self.createQueueScript())  
        outHtml = outHtml.replace("<%readyparams%>", self.createReadyParams())  
        outHtml = outHtml.replace("<%polygonobjects%>", self.model.selectedFormat.createPolygonObjects(self.layersForOutput))
        outHtml = outHtml.replace("<%refineprojection%>", self.model.selectedProjection.refineProjectionScript(self.createMainObject()))
        outHtml = outHtml.replace("<%vectorfeatures%>", self.createVectorFeatures())
        outHtml = outHtml.replace("<%labelfeatures%>", self.createLabelFeatures(self.model.selectedProjection, labels))
        outHtml = outHtml.replace("<%datastore%>", self.createDataStore())
        outHtml = outHtml.replace("<%addlegend%>", self.createLegend())
        outHtml = outHtml.replace("<%tipfunctions%>", self.createTipHelpers())
        outHtml = outHtml.replace("<%symbologyfunctions%>", self.createSymbologyFunctions())
        outHtml = outHtml.replace("<%chartfunction%>", self.createChartFunction(self.model.vizWidth, self.model.vizHeight))
        outHtml = outHtml.replace("<%safecentroidfunction%>", self.createSafeCentroidFunction(self.model.selectedProjection))
        outHtml = outHtml.replace("<%zoomfunction%>", self.createZoomFunction(self.model.selectedProjection, labels))
        
        # overwrite the file with new contents
        f = codecs.open(path, "w", encoding="utf-8")
        
        f.write(outHtml)
        f.close()
    