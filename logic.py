import os
import sys
import inspect
import traceback
import re
import string
import shutil
import time
import codecs
import webbrowser
import zipfile

from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from logger import log
from osHelp import topo
from symbology import *
from projections import *
from bbox import *
from output import *
from viz import *

class model:
    """Model for the UI"""
    
    def __init__(self, iface):
        """Initialise the model"""
        self.__logger = log(self.__class__.__name__)
        self.__colorField = "d3Css"
        self.__cssFile = "color.css"
        self.__selectedFields = []  
        self.__tempVizFields = [] 
        self.__ranges = dataRanges()       
        
        self.iface = iface
        self.title = u""
        self.showHeader = False
        self.width = 800
        self.height = 600
        self.idField = ""
        self.simplification = ""
        self.outputFolder = u""
        self.vectors = []   
        self.projections = [] 
        self.selectedProjection = None  
        self.legend = False
        self.legendPositions = ["Top Left", "Top Right", "Bottom Right", "Bottom Left", "External"]
        self.selectedLegendPosition = 0
        self.popup = False
        self.popupPositions = ["Bubble", "External"]
        self.selectedPopupPosition = 0
        self.panZoom = False
        self.extraVectors = False
        self.topojson = topo()
        self.hasViz = False 
        self.charts = [] 
        self.vizLabels = []  
        self.selectedVizChart = None 
        self.vizWidth = 240
        self.vizHeight = 240   
        self.steradians = ["", 
                           "1e-12", "2e-12", "3e-12", "4e-12", "5e-12", "6e-12", "7e-12", "8e-12", "9e-12", 
                           "1e-11", "2e-11", "3e-11", "4e-11", "5e-11", "6e-11", "7e-11", "8e-11", "9e-11", 
                           "1e-10", "2e-10", "3e-10", "4e-10", "5e-10", "6e-10", "7e-10", "8e-10", "9e-10", 
                           "1e-9", "2e-9", "3e-9", "4e-9", "5e-9", "6e-9", "7e-9", "8e-9", "9e-9", 
                           "1e-8", "2e-8", "3e-8", "4e-8", "5e-8", "6e-8", "7e-8", "8e-8", "9e-8", 
                           "1e-7", "2e-7", "3e-7", "4e-7", "5e-7", "6e-7", "7e-7", "8e-7", "9e-7", 
                           "1e-6", "2e-6", "3e-6", "4e-6", "5e-6", "6e-6", "7e-6", "8e-6", "9e-6", 
                           "1e-5", "2e-5", "3e-5", "4e-5", "5e-5", "6e-5", "7e-5", "8e-5", "9e-5", 
                           "1e-4", "2e-4", "3e-4", "4e-4", "5e-4", "6e-4", "7e-4", "8e-4", "9e-4", 
                           "1e-3", "2e-3", "3e-3", "4e-3", "5e-3", "6e-3", "7e-3", "8e-3", "9e-3" ]
        
        
        # list of tested projections       
        projs = [cls() for cls in projection.__subclasses__()]
        for p in projs:
            self.projections.append(p)
            
        if len(self.projections) > 0:
            self.selectedProjection = self.projections[0]
            
        # list of charts for data viz      
        cs = [cls() for cls in chart.__subclasses__()]      
        for c in cs:
            self.charts.append(c)
            
        if len(self.charts) > 0:
            self.selectedChart = self.charts[0]
           
         
    def hasTopoJson(self):    
        """Does the system have node.js and topojson installed?""" 
        return self.topojson.helper.hasTopojson()
         
    def setup(self): 
        """Get the vector layers from QGIS and perform other startup actions"""
        # Reset
        del self.vectors[:]
        
        layers = iface.legendInterface().layers()
        found = False
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.rendererV2() is not None:
                found = True
                self.vectors.append(vector(self.iface, layer))
                
        # At __init__ the first in the list will be the main vector layer
        if found == True:
            self.vectors[0].main = True
       
    def setSelectedPopupField(self, name, state):
        """Set the selected field state"""
        if state == True:
            if name not in self.__selectedFields:
                self.__selectedFields.append(name)
        else:
            if name in self.__selectedFields:
                self.__selectedFields.remove(name)
                
    def setSelectedVizField(self, name, state):
        """Set the selected viz field state"""
        if state == True:
            if name not in self.__tempVizFields:
                self.__tempVizFields.append(name)
        else:
            if name in self.__tempVizFields:
                self.__tempVizFields.remove(name)
                
    def getCurrentRangeLength(self):
        """Check the length of the current data range"""
        return len(self.__tempVizFields)
                
    def addCurrentRange(self, name):
        """Add the temporary data range to the list"""
        if len(self.__tempVizFields) > 0:
            data = dataRange(name)
            
            for f in self.__tempVizFields:
                data.appendField(f)
                
            self.__ranges.append(data)
            self.__tempVizFields[:] = []
            
    def getDataRangePreview(self):
        """Get the preview of fields in each data range"""
        temp = ""
        
        for data in self.__ranges:
            temp += data.getDisplayString()
            temp += "\r\n"
            
        return temp
        
    def deleteLastRange(self):
        """Remove the last data range from the list"""
        if len(self.__ranges) > 0:
            self.__ranges.pop()
            
    def resetRanges(self):
        """Remove all previously created ranges"""
        self.__ranges[:] = []
        
    def getRangeCount(self):
        """Retrieve the count of data ranges"""
        return len(self.__ranges)
        
    def getVizLabelMask(self):
        """Get the input mask for the data viz labels"""
        return self.__ranges.getQtLabelMask()
            
    def setSelectedLayer(self, name, state):
        """Set the selected extra layer for use in the map"""    
        for v in self.vectors:
            if v.name == name:   
                v.extra = state
        
    def getSelectedLayers(self):
        """Retrieve the selected vector layers"""
        found = []
        for v in self.vectors:
            if v.extra == True:
                found.append(v)
        return found
    
    def setMainLayer(self, index):
        """Set the main layer for use in the map"""
        for v in self.vectors:
            v.main = False
        
        self.vectors[index].main = True
        # also clear the list of selected fields
        self.__selectedFields = []
        
    def getMainLayer(self):
        """Retrieve the selected main vector layer"""
        found = None
        for v in self.vectors:
            if v.main == True:
                found = v
        return found
                
    def setSelectedProjection(self, index):
        """Set the selected projection for use later"""
        for p in self.projections:
            p.selected = False
        
        self.projections[index].selected = True
                
    def getSelectedProjection(self):
        """Retrieve the selected projection"""        
        found = None
        for p in self.projections:
            if p.selected == True:
                found = p
        return found    
    
    def getPopupTemplate(self):
        """Get the default html template for the popup based on the chosen fields"""        
        html = []
        row = "<tr><td>{0}</td><td>{1}</td></tr>\r"
        chart = """<div id="chart" style="width: {0}px; height: {1}px"></div>"""
        
        if len(self.__selectedFields) > 0:
            html.append("<table>\r")
            for f in self.__selectedFields:
                html.append(row.format(f, "{" + f + "}"))
            html.append("</table>")
        
        if self.hasViz == True:
            html.append(chart.format(str(self.vizWidth), str(self.vizHeight)))
        
        return "".join(html)
    
    def getLayersForOutput(self):
        """Get all the layers selected for output in the order defined in the QGIS legend"""
        found = []
        # Get all vecotr layers, extras as well as the main layer
        for v in self.vectors:
            if (self.extraVectors == True and v.extra == True) or v.main == True:
                found.append(v)
        # Reverse the order for processing the output, 
        # this will also form the order the SVG groups are created
        found.reverse()
        return found   
    
    def getUniqueFolderName(self):  
        """Get a unique folder name"""
        return time.strftime("%Y%m%d%H%M%S")          
    
    def setSymbology(self, renderer, layer, index):
        """Read the symbology, generate a CSS style and set against each row in the layers attribute table"""
        
        dump = renderer.dump()        
        self.__logger.info(dump)
        
        transparency = 1 - (float(layer.layerTransparency()) / 100)
        
        if dump[0:6] == "SINGLE":
            return self.setSingleSymbol(layer, renderer, transparency, index)            
        elif dump[0:11] == "CATEGORIZED":
            return self.setCategorizedSymbol(layer, renderer, transparency, index)        
        elif dump[0:9] == "GRADUATED":       
            return self.setGraduatedSymbol(layer, renderer, transparency, index)
        else:
            words = dump.split(" ")
            e = ValueError("{0} renderer in {1} not supported".format(words[0], layer.name))
            raise e 
    
    def setSingleSymbol(self, layer, renderer, transparency, index):
        """Read the symbology for single symbol layers"""      

        self.__logger.info("setSingleSymbol")
        geoType = layer.geometryType()
        syms = symbols()
        cssstub = self.getLayerObjectName(index)
        
        css = cssstub + "r0"
        s = singleSymbol(geoType, renderer.symbol(), css, transparency)     
        syms.append(s)       

        return syms
            
    def setCategorizedSymbol(self, layer, renderer, transparency, index):
        """Read the symbology for categorized symbol layers"""
        
        self.__logger.info("setCategorizedSymbol")
        field = renderer.classAttribute()
        geoType = layer.geometryType()
        cssstub = self.getLayerObjectName(index)
        syms = symbols()
        
        fieldType = "String"
        fields = layer.pendingFields()
        for f in fields:
            if f.name() == field:
                fieldType = f.typeName()    
                break
            
        i = 0
        for c in renderer.categories():
            css = cssstub + "c" + str(i)
            s = categorizedSymbol(geoType, field, fieldType, c, css, transparency)     
            syms.append(s)       
            i += 1
        
        return syms
                            
    def setGraduatedSymbol(self, layer, renderer, transparency, index):
        """Read the symbology for graduated symbol layers"""
        
        self.__logger.info("setGraduatedSymbol")
        field = renderer.classAttribute()
        geoType = layer.geometryType()
        cssstub = self.getLayerObjectName(index)
        syms = symbols()
        
        i = 0
        for r in renderer.ranges():
            css = cssstub + "r" + str(i)
            s = graduatedSymbol(geoType, field, r, css, transparency)     
            syms.append(s)       
            i += 1
            
        return syms
    
    def writeSymbology(self, layer, syms):
        """Write the CSS value to the d3css column"""
        # Create a single transaction for the whole lot
        layer.startEditing() 
        # Loop through each symbol
        if syms is not None:
            for sym in syms:
                filt = sym.getFilterExpression()
                self.__logger.info("Filter: " + filt)
                
                # Get the features with this particular symbology
                features = None
                if len(filt) > 0:
                    features = layer.getFeatures(QgsFeatureRequest().setFilterExpression(filt))
                else: 
                    features = layer.getFeatures()
                    
                # Loop though each feature returned from the filter
                for feature in features:
                    index = layer.fieldNameIndex(self.__colorField)                   
                    layer.changeAttributeValue(feature.id(), index, sym.css)

            # Commit the transaction
            layer.commitChanges()
            
    def getCanvasStyle(self):
        """Get the canvas background color"""
        style = "#mapSvg{{background-color: {0};}}\n"
        return style.format(self.iface.mapCanvas().canvasColor().name())
        
    def writeCss(self, i, uid, syms):
        """Create/append CSS file for symbology"""
        n = self.getDestCssFile(uid)
        f = open(n, "a")
        try:
            # write out the background color on the first iteration through the outer loop
            if i == 0:
                f.write(self.getCanvasStyle())
            # write out all the symbols associated with the layer
            if syms is not None:
                for sym in syms:
                    f.write(sym.getStyle() + "\n");
        except Exception as e:
            # don't leave open files 
            self.__logger.error("Exception\r\n" + traceback.format_exc(None))
            raise e
        finally:
            f.close()
            
    def writeDataFile(self, uid):
        """Write the main info file which will be used in the popup"""
        main = self.getMainLayer()
        features = main.layer.getFeatures()
            
        n = self.getDestDataFile(uid)
        f = codecs.open(n, "a", "utf-8")
        try:
            if self.hasViz == True:
                # Merge the range data with any selected fields
                for range in self.__ranges:
                    fields = range.getFields()
                    for field in fields:
                        if field not in self.__selectedFields:
                            self.__selectedFields.append(field)
            
            # Add the csv header
            if self.idField not in self.__selectedFields:
                self.__selectedFields.append(self.idField)
            
            f.write(u",".join(self.__selectedFields))
            f.write("\n")  
              
            # Loop though each feature and read the values
            for feature in features:
                line = u""
                for field in self.__selectedFields:
                    idField = (field == self.idField)
                    line += self.safeCsvString(feature[field], idField) + ","
                f.write(unicode(line[:-1]))
                f.write(u"\n")
            
        except Exception as e:
            self.__logger.error("Exception\r\n" + traceback.format_exc(None))
            raise e
        finally:
            f.close()
            
    def writeLegendFile(self, uid, syms):
        """Write the legend for the main layer"""
        n = self.getDestLegendFile(uid)
        f = codecs.open(n, "a", "utf-8")
        #for  now a fixed width and height for the legend
        template = u"20,20,{0},{1}\n"
        try:
            if syms is not None:
                f.write("Width,Height,Color,Text\n");
                for sym in syms:
                    uCss = unicode(sym.css)
                    uText = self.safeCsvUnicode(sym.label, False)
                    
                    f.write(template.format(uCss, uText));
                    
        except Exception as e:
            # don't leave open files 
            self.__logger.error("Exception\r\n" + traceback.format_exc(None))
            raise e
        finally:
            f.close()
    
    def safeCsvString(self, obj, idField):
        """Make a string safe from commas and NULLS"""
        val = obj
        if isinstance(obj, unicode) == False:
            val = str(obj)
            
        if val == "NULL":
            val = ""
        if idField == True:
            # d3 strips empty floating points from its id property returning whole numbers
            if val.endswith(".0"):
                val = val[:len(val)-2]        
            
        return val.replace(",","")
        
    def safeCsvUnicode(self, obj, idField):
        """Make a string safe for use in a CSV file
        
        returns unicode formatted string"""
        
        val = obj
        if isinstance(obj, unicode) == False:
            val = unicode(obj, "utf-8")            
        
        return self.safeCsvString(val, idField)
        
            
    def createFolders(self, uid):
        """Create the folder structure and copy code files"""
        src = self.getSourceFolder()
        dest = self.getDestFolder(uid)
        
        try:
            if os.path.isdir(dest):
                # Never going to happen, but just in case... 
                self.log.info("delete previous folder " + dest)
                shutil.rmtree(dest)  

            # Now copy over
            shutil.copytree(src, dest, ignore=self.excludeFiles)
            
        except OSError as e: 
            self.__logger.error(e.args[1])
            
    def excludeFiles(self, dir, files):
        """Don't copy over the file used to force empty directory creation during 
        the plugin distribution as a zip file"""
        
        return {".forcecreation"}
    
    def zipShpFiles(self, uid):
        
        dest = "source.zip"
        path = self.getDestShpFolder(uid)
                
        zipf = zipfile.ZipFile(os.path.join(path, dest), "w")
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != dest:
                    filePath = os.path.join(root, file)
                    zipf.write(filePath, file)
                    os.remove(filePath)
        zipf.close()
            
    def isWindows(self):
        """Windows OS?"""
        return self.topojson.isWindows        
            
    def getSourceFolder(self):
        """Get the plugin html source"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "html")
    
    def getDestFolder(self, uid):
        """Get the destination folder with the unique id appended"""
        safeFolder = self.outputFolder
        if self.isWindows() == True:
            safeFolder = self.outputFolder.encode('ascii', 'ignore')

        return os.path.join(safeFolder, uid)
       
    def getUniqueFilePath(self, fullPath):
        """Get a unique full path to a file"""
        if os.path.exists(fullPath):
            
            path, name = os.path.split(fullPath)
            name, ext = os.path.splitext(name)    
            make = lambda i: os.path.join(path, '%s(%d)%s' % (name, i, ext))
    
            for i in xrange(2, sys.maxint):
                fullPath = make(i)
                if not os.path.exists(fullPath):
                    break
                
        return fullPath
    
    def getDestShpFile(self, uid, layer):
        """Get the destination path to the shapefile"""
        dest = self.getDestShpFolder(uid)
        
        fullPath = self.getUniqueFilePath(os.path.join(dest, layer.name + ".shp"))
        
        return fullPath
    
    def getDestShpFolder(self, uid):
        """Get the destination shapefile folder path"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "shp")
    
    def getDestIndexFile(self, uid):
        """Get the destination index file path"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "index.html")
    
    def getDestCssFile(self, uid):
        """Get the destination CSS file path"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "css", self.__cssFile)
    
    def getDestDataFile(self, uid):
        """Get the destination info file path"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "data/info.csv")
    
    def getDestLegendFile(self, uid):
        """Get the destination legend file path"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "data/legend.csv")
    
    def getDestTopoFolder(self, uid):
        """Get the destination shapefile folder"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "topo")
    
    def addColorColumn(self, layer):
        """Add a new column to hold the color used in symbology"""
        if self.hasField(layer, self.__colorField) == False:
            self.addField(layer, self.__colorField)
            
    def addField(self, layer, name):
        """Add a new column to the layer data provider with the given name"""
        self.__logger.info("Adding field: " + name)
        
        layer.startEditing()
        
        provider = layer.dataProvider()
        provider.addAttributes([ QgsField(name, QVariant.String) ])
        
        layer.commitChanges()
            
    def hasField(self, layer, name):
        """Does a particular field already exist?"""
        result = False
        
        if layer.fieldNameIndex(name) > -1:
            result = True
        '''fields = layer.pendingFields()
        for f in fields:
            if f.name() == name:
                result = True
                break'''
        
        return result
    
    def saveShape(self, uid, vect):
        """Save the shapefile in WGS84 with new color column"""       
        crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        QgsVectorFileWriter.writeAsVectorFormat(vect.layer,
                                                vect.filePath,
                                                "system",
                                                crs,
                                                "ESRI Shapefile")
                                                        
    def getSafeString(self, val):
        """Return a string condsidered safe for use in file names"""
        pattern = re.compile('[\W_]+', re.UNICODE)
        return pattern.sub("", val)                                                
        
    def getLayerObjectName(self, index):
        """Get a unique layer name as an object within topojson"""
        return "l" + str(index)
    
    def getProgressTicks(self):
        """Get the amount of progress steps"""
        layers = self.getLayersForOutput()
        return 3 + (7 * len(layers))
        
    def areLayersModified(self):
        """Have the chosen layers been modified?"""
        isEdit = False
        
        layers = self.getLayersForOutput()
        for vect in layers:    
            if vect.layer.isEditable() == True and vect.layer.isModified() == True:
                isEdit = True
                break
            
        return isEdit
    
    def logExportParams(self, main):
        """Log the parameters to the log messages panel"""
        template = u"       {0} = [{1}]"
        
        self.__logger.info(template.format("Title", self.title))
        self.__logger.info(template.format("Header", str(self.showHeader)))
        self.__logger.info(template.format("Width", str(self.width)))
        self.__logger.info(template.format("Height", str(self.height)))
        self.__logger.info(template.format("Main layer", main.name))
        self.__logger.info(template.format("IDField", self.idField))
        self.__logger.info(template.format("Projection", self.selectedProjection.name))
        self.__logger.info(template.format("Simplify", self.simplification))
        self.__logger.info(template.format("Output", self.outputFolder))
        self.__logger.info(template.format("Zoom/Pan", str(self.panZoom)))
        self.__logger.info(template.format("Legend", str(self.legend)))
        self.__logger.info(template.format("LegendPos", self.legendPositions[self.selectedLegendPosition]))
        
        extras = []
        layers = self.getLayersForOutput()
        for l in layers:
            extras.append(l.name)
        self.__logger.info(template.format("IncExtras", str(self.extraVectors)))
        self.__logger.info(template.format("Extras", ", ".join(extras)))
        
        self.__logger.info(template.format("IncPopup", str(self.popup)))
        self.__logger.info(template.format("PopupPos", self.popupPositions[self.selectedPopupPosition]))
        self.__logger.info(template.format("Popup", self.getPopupTemplate()))
        
        self.__logger.info(template.format("IncViz", str(self.hasViz)))
        self.__logger.info(template.format("Chart", self.selectedVizChart.name))
        self.__logger.info(template.format("VizWidth", str(self.vizWidth)))
        self.__logger.info(template.format("DataRanges", self.getDataRangePreview()))  
        self.__logger.info(template.format("Labels", ", ".join(self.vizLabels)))       

        
    def export(self, progress):
        """Main export function. Do the stuff.
        
        :param progress: Progress bar widget.
        :type progress: QProgressBar
        """
        tick = 0
        progress.setValue(tick)
        
        main = self.getMainLayer()
        
        if main is not None:        
            self.__logger.info("EXPORT start ==================================================")
            self.logExportParams(main)
            
            # Create a class to help in replacing all the JavaScript in the index.html file
            outVars = outputVars(main.layer, self.showHeader, self.idField, 
                                 (self.selectedPopupPosition == 1), 
                                 self.legend, self.panZoom, self.selectedLegendPosition,
                                 self.selectedVizChart, self.__ranges, self.vizLabels) 

            # Create the directory structure
            self.__logger.info("EXPORT copying folders and files")
            uid = self.getUniqueFolderName()
            self.createFolders(uid)
        
            tick+=1
            progress.setValue(tick)
            
            # Get layers in correct order
            layers = self.getLayersForOutput()
            i = 0
            for vect in layers:     
                self.__logger.info("EXPORT " + vect.name)   
                vect.filePath = self.getDestShpFile(uid, vect)
                
                renderer = vect.layer.rendererV2()
                
                # Save shapefile with WSG84 coordinates
                self.saveShape(uid, vect)
                tick+=1
                progress.setValue(tick)
                
                # Re-open saved shape file now its available for editing                               
                destLayer = QgsVectorLayer(vect.filePath, vect.name, "ogr")
            
                # Add a color column
                self.addColorColumn(destLayer)
                tick+=1
                progress.setValue(tick)
                
                # Read colors
                syms = self.setSymbology(renderer, destLayer, i)
                tick+=1
                progress.setValue(tick)
            
                # Write colors
                self.writeSymbology(destLayer, syms)
                tick+=1
                progress.setValue(tick)
                
                # Close the shapefile
                del destLayer
                
                # Write CSS file
                self.writeCss(i, uid, syms)  
                tick+=1
                progress.setValue(tick)
                          
                # Create the topojson file
                # And then store the details in order to write the index file
                objName, name, bbox = self.output(uid, vect, i)
                hasTip = vect.main and self.popup  
                hasViz = vect.main and self.hasViz
                outlineWidth = syms.getAvergageOutlineWidth()     
                
                tick+=1
                progress.setValue(tick)         
                
                outVars.outputLayers.append(outputLayer(objName, name, outlineWidth, vect.main, hasTip, hasViz))
                outVars.bboxes.append(bbox)
                
                if self.legend and vect.main:
                    # Create the legend for the main layer
                    self.writeLegendFile(uid, syms)  
                    
                tick+=1
                progress.setValue(tick)              
                
                i+=1
                  
            
            # Alter the index file
            index = self.writeIndexFile(uid, outVars)
            tick+=1
            progress.setValue(tick)
            
            # Order of things is important
            # writeDataFile() appends an ID field if not already in the popup
            # Would result in the popup template potentially having an unexpected ID field
            if self.popup == True or self.hasViz == True:
                self.__logger.info("EXPORT popup data")
                # Create the data files
                self.writeDataFile(uid) 
            
            # Now zip up the shapefiles
            self.zipShpFiles(uid)
            
            self.__logger.info("EXPORT complete =========================================================")
            
            tick+=1
            progress.setValue(tick)
                
            # start browser
            # TODO: Create separate settings dialog
            # TODO: Option of opening file browser
            # TODO: Option of specifying a web server URL
            webbrowser.open_new_tab("http://127.0.0.1:8080/{0}/index.html".format(uid))
    
    def writeIndexFile(self, uid, outVars):
        """Read and write the index html file"""
        n = self.getDestIndexFile(uid)
        f = codecs.open(n, "r", encoding="utf-8")        
        # Get the contents of the file
        html = f.read()
        f.close()
            
        proj = self.selectedProjection.toScript(outVars.bboxes.getMaxBound(), self.width, self.height)
        self.__logger.info(proj)
        
        # Can't use string format as it has a fit over css and javascript braces {}
        outHtml = u""
        outHtml = html.replace("<%title%>", self.title)
        outHtml = outHtml.replace("<%header%>", outVars.createHeader(self.title))
        outHtml = outHtml.replace("<%tooltiptemplate%>", self.getPopupTemplate())
        outHtml = outHtml.replace("<%externallegend%>", outVars.createExtLegend())
        outHtml = outHtml.replace("<%externaltip%>", outVars.createExtTip())
        outHtml = outHtml.replace("<%width%>", str(self.width))
        outHtml = outHtml.replace("<%height%>", str(self.height))
        outHtml = outHtml.replace("<%projection%>", proj)
        outHtml = outHtml.replace("<%vectorpaths%>", outVars.createSvgPaths())
        outHtml = outHtml.replace("<%attachzoom%>", outVars.createZoom())
        outHtml = outHtml.replace("<%hidetip%>", outVars.hideTip())
        outHtml = outHtml.replace("<%attachtip%>", outVars.createTipFunction())
        outHtml = outHtml.replace("<%queuefiles%>", outVars.createQueueScript())  
        outHtml = outHtml.replace("<%readyparams%>", outVars.createReadyParams())  
        outHtml = outHtml.replace("<%polygonobjects%>", outVars.createPolygonObjects())
        outHtml = outHtml.replace("<%mainobject%>", outVars.createMainObject())
        outHtml = outHtml.replace("<%vectorfeatures%>", outVars.createVectorFeatures())
        outHtml = outHtml.replace("<%datastore%>", outVars.createDataStore())
        outHtml = outHtml.replace("<%addlegend%>", outVars.createLegend())
        outHtml = outHtml.replace("<%tipfunctions%>", outVars.createTipHelpers())
        outHtml = outHtml.replace("<%chartfunction%>", outVars.createChartFunction(self.vizWidth, self.vizHeight))
        outHtml = outHtml.replace("<%zoomfunction%>", outVars.createZoomFunction())
        
        # overwrite the file with new contents
        f = codecs.open(n, "w", encoding="utf-8")
        
        f.write(outHtml)
        f.close()
                        
        return n
        
    def output(self, uid, layer, index):
        """Output a shapefile to topojson"""   
        path = self.getDestTopoFolder(uid)         
        name = self.getSafeString(layer.name)  
        
        fullPath = self.getUniqueFilePath(os.path.join(path, name + ".json"))
        
        path, name = os.path.split(fullPath)
        name, ext = os.path.splitext(name) 
        
        objName = self.getLayerObjectName(index)  
        
        quantization = ""
        #if self.panZoom:
        #    quantization = "1e5"
        
        result = self.topojson.helper.output(self.getDestTopoFolder(uid), 
                                name, 
                                objName, 
                                layer.filePath, 
                                quantization,
                                self.simplification, 
                                self.idField, 
                                [self.__colorField])
        
        matches = result.split()
        
        return objName, name, bound(float(matches[1]), float(matches[2]), float(matches[3]), float(matches[4]))
        
    
class vector:
    """Base class for the layer abstracting away the QGIS details"""
    
    def __init__(self, iface, layer):
        """Initialise the layer"""
        
        self.rendererType = 0
        self.id = layer.id
        self.name = layer.name()
        self.layer = layer
        self.filePath = ""
        self.main = False
        self.extra = iface.legendInterface().isLayerVisible(layer)
        self.type = layer.type()
        self.fields = []
        self.vizFields = []
        self.defaultId = ""
        self.isVisible = iface.legendInterface().isLayerVisible(layer) 
        for f in layer.pendingFields():
            # Add to the list of fields
            self.fields.append(f.name()) 
            
            # Add numeric fields to the list for visualization
            if f.typeName() == "Integer" or f.typeName() == "Real":
                self.vizFields.append(f.name())
            
            # An ID field? Set the default for the ID field option    
            upper = f.name().upper() 
            if upper == "ID" or upper == "OBJECT_ID" or upper == "OBJECTID":
                self.defaultId = upper
                
                
        renderer = layer.rendererV2()
        dump = renderer.dump()
        
        if dump[0:6] == "SINGLE":
            self.rendererType = 0            
        elif dump[0:11] == "CATEGORIZED":
            self.rendererType = 1        
        elif dump[0:9] == "GRADUATED":
            self.redererType = 2
            
    def isSingleRenderer(self):
        """Is this a single renderer type?"""
        return self.rendererType == 0