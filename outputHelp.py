import codecs
import os

from bbox import *
from viz import *
from qgis.core import *
from osHelp import osHelper
from logger import log
from gisWrapper import *
from labelHelper import *

class outputVars(object):
    """Struct to pass variables from the model to functions which generate the html for the d3 map"""
    
    def __init__(self, main, title, width, height, hasHeader, idField, extTip, 
                 hasLegend, allowZoom, legendPosition, chartType, ranges, labels,
                 vizHeight, vizWidth, showLabels):
        """Constructor"""
        self.mainLayer = main
        self.title = title
        self.width = width
        self.height = height
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
        self.vizHeight = vizHeight 
        self.vizWidth = vizWidth 
        self.showLabels = showLabels
        

class outFormat(object):
    """Base object to parse Html for the Output Format.
    Due to historic reasons this is essentially TopoJson."""
    
    def __init__(self):
        """Base Constructor"""
        self.name = u""
        self.extension = u".json"
        
        self.outVars = None
        self.__logger = log(self.__class__.__name__)
    
    def convertShapeFile(self, destFolder, destPath, sourcePath, objName, simplification, idField, idAttribute, preserveAttributes):
        """Base implementation - does nothing"""
        raise NotImplementedError("Abstract method requires calling of override on derived class")  
    
    def getPopupTemplate(self, selectedFields, hasViz, vizWidth, vizHeight):
        """Get the default html template for the popup based on the chosen fields"""        
        html = []
        row = "<tr><td>{0}</td><td>{1}</td></tr>\r"
        chart = """<div id="chart" style="width: {0}px; height: {1}px"></div>"""
        
        if len(selectedFields) > 0:
            html.append("<table>\r")
            for f in selectedFields:
                html.append(row.format(f, "{" + f + "}"))
            html.append("</table>")
        
        if hasViz == True:
            html.append(chart.format(str(vizWidth), str(vizHeight)))
        
        return "".join(html)
        
    def tipInUse(self):
        """Is there a tip or chart in one of the layers"""
        tip = False
        for o in self.outVars.outputLayers:            
            if o.hasTip == True or o.hasViz == True:
                tip = True
            
        return tip
    
    def vizInUse(self):
        """Is there a chart in one of the layers"""
        viz = False
        for o in self.outVars.outputLayers:            
            if o.hasViz == True:
                viz = True
            
        return viz
            
        
    def createHeader(self, title):
        """Creating the optional heading element"""
        template = u"<h1>{0}</h1>"
        
        if self.outVars.hasHeader == True:
            return template.format(title)
        else:
            return ""
        
    def createSvgPaths(self, labels, selectedProjection):
        """Create the Svg group and path elements required by the layers"""
        paths = []
        template = "    var vectors{index} = vectors.append(\"g\");\n    var vector{index} = void 0;\n"
        i = 0
        for i, o in enumerate(self.outVars.outputLayers):
            path = template.format( index = i )
            paths.append(path)
            paths.append(o.firstSymbol.safeSvgNode(selectedProjection.safeCentroid))

        if self.outVars.showLabels == True:
            labelTemplate = """    var label{index} = void 0;"""
            for l in labels:
                if l.hasLabels() == True:
                    path = labelTemplate.format( index = l.index )
                    paths.append(path)
         
            
    
        return "".join(paths)
    
    def createZoom(self, selectedProjection):
        """Create the JavaScript function to zoom"""
        if self.outVars.allowZoom:
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
            if self.outVars.extTip == True:
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
            value = self.outVars.chartType.getJavaScript(self.outVars.mainLayer, self.outVars.vizRanges, self.outVars.vizLabels, vizWidth, vizHeight, self.outVars.extTip)

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
            val = template.replace("<%idfield%>", self.outVars.idField)
            cobj = ""
            if self.vizInUse() == True:
                cobj = "chart(obj);"
            val = val.replace("<%chart%>", cobj)
                
        return val

    def createSymbologyFunctions(self):
        """Create the necessary helper functions for symbology to display correctly"""
        scripts = []
        
        for o in self.outVars.outputLayers:
            script = o.firstSymbol.getAdditionalScripts()
            # Ensure items in the list are unique 
            if script != "" and script not in scripts:
                scripts.append(script)                
        
        return "".join(scripts)
     
    def createSafeCentroidFunction(self, selectedProjection):
        """Create the JavaScript centroid helper function"""       
     
        if self.outVars.allowZoom == True and selectedProjection.safeCentroid == True:
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
     
        if self.outVars.allowZoom == True:

            if self.tipInUse() == True:
                template = template.replace("<%hidetip%>", "hideTip();")
            else:
                template =  template.replace("<%hidetip%>", "")
                
            ''' Zoom scaling script '''     
            v = []
            
            ''' Projection wide scaling script '''
            v.append(selectedProjection.zoomScalingScript())
            
            ''' Symbol specific scaling script '''
            for o in self.outVars.outputLayers:
                v.append(o.firstSymbol.zoomScalingScript(selectedProjection.safeCentroid))
                
            template = template.replace("<%vectorscaling%>", "".join(v))
            
            ''' Label scaling '''
            if self.outVars.showLabels == True:
                                
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
        i = 0
        for o in self.outVars.outputLayers:               
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
        for o in self.outVars.outputLayers:             
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
        for o in self.outVars.outputLayers:
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
        for o in self.outVars.outputLayers:
            if o.isMain:
                output = template.format(index = i)
                break
            i += 1
            
        return output
                
    
    def createVectorFeatures(self, selectedProjection):
        """Create the polygon vector features"""
        
        scripts = []
        template = """      vector{index} = vectors{index}.selectAll("path").data(object{index}.features);
      vector{index}.enter()
        .append("path")\n"""
        main = """        .attr("id", function (d) {{ return d.id; }})\n"""
        static = """        .attr("class", function (d) {{ return d.properties.d3Css; }})"""
        tip = """\n        .on("click", function (d) {{ return showTip(d.id); }});\n\n"""
        
        for i, o in enumerate(self.outVars.outputLayers):
            layerScript = []
            script = template.format(
                index = i
            )
            layerScript.append(script)
            if o.isMain == True:
                layerScript.append(main)
            layerScript.append("{0}")
            layerScript.append(static)

            if o.hasTip == True or o.hasViz == True:
                layerScript.append(tip)
            else:
                layerScript.append(";\n\n")
            
            scripts.append(o.firstSymbol.toLayerScript( "".join(layerScript), selectedProjection.safeCentroid ) )     
    
        return "".join(scripts)
    
    def createLabelFeatures(self, selectedProjection, labels):
        """Create the label features"""
        scripts = []
        
        if self.outVars.showLabels == True:            
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
        if self.outVars.hasLegend:
            template = """      }}
      var legend = d3.legend({s})
        .csv("data/legend.csv")
        .position({p})
        .shape(RECT);
      {s}.call(legend);"""

            ext = ""
            svg = "svg"
            pos = self.outVars.selectedLegendPosition
                  
            if self.outVars.selectedLegendPosition == 4:
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
        if self.outVars.hasLegend == True and self.outVars.selectedLegendPosition == 4:
            return """  <div id="extLgnd"></div>"""
        else:
            return ""
        
    def createExtTip(self):
        """Add a placeholder for the external tip"""
        if self.tipInUse() == True and self.outVars.extTip == True:
            return """  <div id="extTip"></div>"""
        else:
            return ""        
 
    def writeIndexFile(self, path, outVars, bound, selectedProjection, selectedFields, labels):
        """Read and write the index html file"""
        self.outVars = outVars
        
        f = codecs.open(path, "r", encoding="utf-8")        
        # Get the contents of the file
        html = f.read()
        f.close()
        
        # Can't use string format as it has a fit over css and javascript braces {}
        outHtml = u""
        outHtml = html.replace("<%title%>", self.outVars.title)
        outHtml = outHtml.replace("<%header%>", self.createHeader(self.outVars.title))
        outHtml = outHtml.replace("<%tooltiptemplate%>", self.getPopupTemplate(selectedFields, self.vizInUse(), self.outVars.vizWidth, self.outVars.vizHeight))
        outHtml = outHtml.replace("<%externallegend%>", self.createExtLegend())
        outHtml = outHtml.replace("<%externaltip%>", self.createExtTip())
        outHtml = outHtml.replace("<%width%>", str(self.outVars.width))
        outHtml = outHtml.replace("<%height%>", str(self.outVars.height))
        outHtml = outHtml.replace("<%projection%>", selectedProjection.toScript(bound, self.outVars.width, self.outVars.height))
        outHtml = outHtml.replace("<%vectorpaths%>", self.createSvgPaths(labels, selectedProjection))
        outHtml = outHtml.replace("<%attachzoom%>", self.createZoom(selectedProjection))
        outHtml = outHtml.replace("<%hidetip%>", self.hideTip())
        outHtml = outHtml.replace("<%attachtip%>", self.createTipFunction())
        outHtml = outHtml.replace("<%queuefiles%>", self.createQueueScript())  
        outHtml = outHtml.replace("<%readyparams%>", self.createReadyParams())  
        outHtml = outHtml.replace("<%polygonobjects%>", self.createPolygonObjects())
        outHtml = outHtml.replace("<%refineprojection%>", selectedProjection.refineProjectionScript(self.createMainObject()))
        outHtml = outHtml.replace("<%vectorfeatures%>", self.createVectorFeatures(selectedProjection))
        outHtml = outHtml.replace("<%labelfeatures%>", self.createLabelFeatures(selectedProjection, labels))
        outHtml = outHtml.replace("<%datastore%>", self.createDataStore())
        outHtml = outHtml.replace("<%addlegend%>", self.createLegend())
        outHtml = outHtml.replace("<%tipfunctions%>", self.createTipHelpers())
        outHtml = outHtml.replace("<%symbologyfunctions%>", self.createSymbologyFunctions())
        outHtml = outHtml.replace("<%chartfunction%>", self.createChartFunction(self.outVars.vizWidth, self.outVars.vizHeight))
        outHtml = outHtml.replace("<%safecentroidfunction%>", self.createSafeCentroidFunction(selectedProjection))
        outHtml = outHtml.replace("<%zoomfunction%>", self.createZoomFunction(selectedProjection, labels))
        
        # overwrite the file with new contents
        f = codecs.open(path, "w", encoding="utf-8")
        
        f.write(outHtml)
        f.close()       

class topoJson(outFormat):
    """Functions required to parse the html index file for TopoJson"""
    
    def __init__(self):
        """TopoJson Constructor"""
        self.name = u"TopoJson"
        self.extension = u".json"
        
        self.outVars = None
        self.osHelp = osHelper()
        self.__logger = log(self.__class__.__name__)


    def convertShapeFile(self, destFolder, destPath, sourcePath, objName, simplification, idAttribute, preserveAttributes):
        """Output a shapefile to topojson"""   
        path, name = os.path.split(destPath)
        name, ext = os.path.splitext(name)          
        
        quantization = ""
        #if self.panZoom:
        #    quantization = "1e5"
        
        result = self.osHelp.helper.output(destFolder, 
                                name, 
                                objName, 
                                sourcePath, 
                                quantization,
                                simplification, 
                                idAttribute, 
                                preserveAttributes)
            
        return objName, name
                         

class geoJson(outFormat):
    """Functions required to parse the html index file for GeoJson"""

    def __init__(self):    
        """GeoJson Constructor"""
        self.name = u"GeoJson"
        self.extension = u".json"
        
        self.__qgis = qgisWrapper()
        self.outVars = None    
        self.__logger = log(self.__class__.__name__)

    def convertShapeFile(self, destFolder, destPath, sourcePath, objName, simplification, idAttribute, preserveAttributes):
        """Output a shapefile to GeoJson"""          
        path, name = os.path.split(destPath)
        name, ext = os.path.splitext(name) 
        
        qgisLayer = self.__qgis.openShape(sourcePath, objName)
        
        # Combine the list of attributes to preserve
        if idAttribute != "":
            preserveAttributes.append(idAttribute)
        
        self.__qgis.removeFields(qgisLayer, preserveAttributes)
        
        # Calculate precision from selected steradian / 15     
        #precision = round(15 - (15 / len(self.steradians)) * (self.steradians.index(self.steradian) + 1))
        
        
        QgsVectorFileWriter.writeAsVectorFormat(qgisLayer, 
                                                destPath, 
                                                "utf-8", 
                                                self.__qgis.getDefaultCrs(), 
                                                "GeoJson", 
                                                False, 
                                                layerOptions=['COORDINATE_PRECISION=15'])
        
        return objName, name
        
    def createPolygonObjects(self):
        """Create the Svg polygon objects"""
        scripts = []
        template = "      var object{index} = json{index};\n"
        i = 0
        for o in self.outVars.outputLayers:
            script = template.format(
                index = i
            )
            scripts.append(script)
            i += 1
    
        return "".join(scripts)
    
    def createVectorFeatures(self):
        """Create the polygon vector features"""
        scripts = []
        template = """      vector{index} = vectors{index}.selectAll("path").data(object{index}.features);
      vector{index}.enter()
        .append("path")\n"""
      
        main = """        .attr("id", function (d) {{ return d.properties.""" + self.outVars.idField + """; }})\n"""
        static = """        .attr("class", function (d) {{ return d.properties.d3Css; }})"""
        tip = """\n        .on("click", function (d) {{ return showTip(d.properties.""" + self.outVars.idField + """); }});\n\n"""
        
        i = 0
        for o in self.outVars.outputLayers:
            layerScript = []
            script = template.format(
                index = i
            )
            layerScript.append(script)
            if o.isMain == True:
                layerScript.append(main)
            layerScript.append("{0}")
            layerScript.append(static)

            if o.hasTip == True or o.hasViz == True:
                layerScript.append(tip)
            else:
                layerScript.append(";\n\n")
            
            scripts.append(o.firstSymbol.toLayerScript( "".join(layerScript) ) )    
            i += 1
    
        return "".join(scripts)       
    
    
class outputLayer:
    """Details of layer details for the d3 map"""
    
    def __init__(self, objName, name, averageWidth, main, hasTip, hasViz, syms):
        """Abstract object containing the details required during creation of the inddex.html file 
               
        :param objName: Abstract key for the layer in the form "l" + index in output.
        :type objName: str
        
        :param name: The name given to the layer in the QGIS legend
        :type name: str
        
        :param averageWidth: Average outline width for items in the layer
        :type averageWidth: float
        
        :param main: Is this the main layer for the visualisation?
        :type main: bool
        
        :param hasTip: Does this visualisation include tool tips?
        :type hasTip: bool
        
        :param hasViz: Does this visualisation include charts?
        :type hasViz: bool
        
        :param syms: Symbols used in this layer (only interested in the first symbol as d3 does not allow for different symbol types on a single layer)
        :type syms: array of d3MapRenderer.symbology.singleSymbol (or inherited object)
        """
        self.objName = objName
        self.name = name
        self.isMain = main
        self.hasTip = hasTip
        self.hasViz = hasViz
        self.strokeWidth = averageWidth
        # TODO: Attach renderer object and all symbols
        self.firstSymbol = syms[0].symbol
        
        