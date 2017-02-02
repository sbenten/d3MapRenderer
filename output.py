import os

from qgis.core import *
from osHelp import osHelper
from logger import log
from gisWrapper import *
        

class supportedFormat(object):
    """Base object to parse Html for the Output Format.
    Due to historic reasons this is essentially TopoJson."""           
    def __init__(self):
        """Base Constructor"""
        self.name = u""
        self.extension = u".json"

        self.__logger = log(self.__class__.__name__)        
        
         
    def convertShapeFile(self, destFolder, destPath, sourcePath, objName, simplification, idField, idAttribute, preserveAttributes):
        """Base implementation - does nothing"""
        raise NotImplementedError("Abstract method requires calling of override on derived class")  
    
    def createPolygonObjects(self, layersForOutput):
        """Base implementation - does nothing"""
        raise NotImplementedError("Abstract method requires calling of override on derived class") 
        
    def createVectorFeatures(self, selectedProjection, layersForOutput):
        """Base implementation - does nothing"""
        raise NotImplementedError("Abstract method requires calling of override on derived class") 
        
    def convertToJson(self, destFolder, destPath, sourcePath, objName, simplification, idAttribute, preserveAttributes, precision):
        """Output a shapefile to GeoJson"""          
        path, name = os.path.split(destPath)
        name, ext = os.path.splitext(name) 
        
        qgis = qgisWrapper()
        qgisLayer = qgis.openShape(sourcePath, objName)
        
        # Combine the list of attributes to preserve
        if idAttribute != "":
            preserveAttributes.append(idAttribute)
        
        qgis.removeFields(qgisLayer, preserveAttributes)
        
        
        QgsVectorFileWriter.writeAsVectorFormat(qgisLayer, 
                                                destPath, 
                                                "utf-8", 
                                                qgis.getDefaultCrs(), 
                                                "GeoJson", 
                                                False, 
                                                layerOptions=['COORDINATE_PRECISION={0}'.format(precision)])
        
        return objName, name
    
    def getPopupTemplate(self, selectedFields, hasViz, vizWidth, vizHeight):
        """Get the default html template for the popup based on the chosen fields"""   
        # TODO: Why is this here? SHouldbe in html.py     
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

class topoJson(supportedFormat):
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
        
        """To work with both version 1 and 2 of the topojson command line
        first convert the shapefile to geojson and then convert to topojson""" 
        
        """1. Convert to GeoJson
        Use a destination path with a *_geo.json name for the filename"""
        path, file = os.path.split(destPath)
        orig, ext = os.path.splitext(file) 
        
        geoDestPath = os.path.join(path, orig + "_geo" + ext)
        
        objName, name = self.convertToJson(destFolder, geoDestPath, sourcePath, objName, simplification, idAttribute, preserveAttributes, "15")        
        
         
        
        """2. Convert to TopoJson"""
        quantization = ""
        #if self.panZoom:
        #    quantization = "1e5"
        #folder, outFile, inFile, quantization, simplification
        result = self.osHelp.helper.output(destFolder, 
                                orig,
                                objName, 
                                geoDestPath, 
                                quantization,
                                simplification)
        
        self.__logger.info(result)
            
        return objName, orig
    
    # TODO: Move to d3MapRenderer.html.index  
    def createPolygonObjects(self, layersForOutput):
        """Create the Svg polygon objects"""
        scripts = []
        template = "      var object{index} = topojson.feature(json{index}, json{index}.objects.l{index});\n"
        i = 0
        for o in layersForOutput:
            script = template.format(
                index = i
            )
            scripts.append(script)
            i += 1
    
        return "".join(scripts)


class geoJson(supportedFormat):
    """Functions required to parse the html index file for GeoJson"""

    def __init__(self):    
        """GeoJson Constructor"""
        self.name = u"GeoJson"
        self.extension = u".json"
        
        self.outVars = None    
        self.__logger = log(self.__class__.__name__)

    def convertShapeFile(self, destFolder, destPath, sourcePath, objName, simplification, idAttribute, preserveAttributes):
        """Convert to default GeoJson"""
        return self.convertToJson(destFolder, destPath, sourcePath, objName, simplification, idAttribute, preserveAttributes, "15")
        
    def createPolygonObjects(self, layersForOutput):
        """Create the Svg polygon objects"""
        scripts = []
        template = "      var object{index} = json{index};\n"
        i = 0
        for o in layersForOutput:
            script = template.format(
                index = i
            )
            scripts.append(script)
            i += 1
    
        return "".join(scripts)       