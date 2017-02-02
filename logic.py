import os
import sys
import inspect
import traceback
import string
import shutil
import time
import codecs
import webbrowser
import zipfile

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from logger import log

from osHelp import osHelper
from symbology import *

from bbox import *
from d3MapRenderer.output import *
from html import index
from viz import *
from gisWrapper import *
from labelHelper import labeling

  
class process(object):
    """Class to perform the conversion of the shapefiles to selected format and 
       create the output files"""
    def __init__(self, model):
        """Initialise the process object        
                
        :param model: The UI model for all entered data.
        :type model: d3MapRenderer.logic.model
        """
        self.__logger = log(self.__class__.__name__)
        self.__colorField = "d3Css"
        self.__sizeField = "d3S"
        self.__cssFile = "color.css" 
        
        self.__qgis = qgisWrapper()
        self.osHelp = osHelper()  
        self.model = model
        self.htmlWriter = index()
           
    def export(self, progress, webServerUrl):
        """Main export function. Do the stuff.
        
        :param progress: Progress bar widget.
        :type progress: QProgressBar

        
        :param webServerUrl: Url for displaying the resulting output to d3 in the web browser.
        :type webServerUrl: String
        """
        tick = 0
        progress.setValue(tick)
        
        main = self.model.getMainLayer()
        
        if main is not None:        
            self.__logger.info("EXPORT start ==================================================")
            self.model.logData()
            
            # Initialise bounding box for projection 
            bbox = bound()

            # Create the directory structure
            self.__logger.info("EXPORT copying folders and files")
            uid = self.getUniqueFolderName()
            self.createFolders(uid)
        
            tick += 1
            progress.setValue(tick)
            
            # List for all QgsVectorLayers symbology
            symbols = []
            
            # List for all QgsVectorLayers label styles
            labels = [] 

            for i, vect in enumerate( self.model.getLayersForOutput()):     
                self.__logger.info("EXPORT " + vect.name)   
                vect.filePath = self.getDestShpFile(uid, vect)
                
                # Update vect.symbols with output order 
                vect.setOutputOrder(i)
                
                # Save the open layer in the output directory and in the WGS84 projection for conversion to Geo/topojson
                self.__qgis.saveShape(vect.layer, vect.filePath)

                tick += 1
                progress.setValue(tick)
                
                # Re-open saved shape file now its available for editing 
                destLayer = self.__qgis.openShape(vect.filePath, vect.name)                              
            
                # Read the extent of the layer now its in the correct crs
                if vect.main == True:
                    extent = destLayer.extent()
                    bbox.setLeft(extent.xMinimum())
                    bbox.setBottom(extent.yMinimum())
                    bbox.setRight(extent.xMaximum())
                    bbox.setTop(extent.yMaximum())
            
                # Add a color column
                self.addColumns(destLayer)
                tick += 1
                progress.setValue(tick)
            
                # Write color column to the QgsVectorLayer
                self.writeSymbology(destLayer, vect.renderers)
                tick += 1
                progress.setValue(tick)
                
                # Close the shapefile
                del destLayer
                
                # Determine the attributes to preserve from the shapefile
                # Limited to color, id and label fields
                # Popup attributes are preserved in a CSV file                
                preserveAttributes = [self.__colorField, self.__sizeField]
                
                # Get any labels for the QgsVectorLayer
                label = labeling(vect.layer, i)
                if self.model.showLabels == True and label.hasLabels() == True:
                    labels.append(label)
                    preserveAttributes.append(label.fieldName)
                
                tick += 1
                progress.setValue(tick)                          
            
                # Only output the id field for the main layer
                idAttribute = ""
                if vect.main == True:
                    idAttribute = self.model.idField        
        
                # Create the output json file
                path = self.getDestJsonFolder(uid)         
                name = vect.getSafeName()
                                
                # And then store the details in order to write the index file
                destPath = self.getUniqueFilePath(os.path.join(path, name + self.model.selectedFormat.extension))
                objName, name = self.model.selectedFormat.convertShapeFile(path, destPath, vect.filePath, vect.getLayerObjectName(i), self.model.simplification, idAttribute, preserveAttributes)
                
                # Store some properties on the vectore layer
                # TODO: IS this still the referred to layer, or a shallow copy?
                vect.hasTip = vect.main and self.model.popup  
                vect.hasViz = vect.main and self.model.hasViz
                vect.outlineWidth = vect.renderers.getAvergageOutlineWidth()    
                
                # Store the QgsVectorLayer symbols in a single list now that the the average outline width has been calculated
                symbols.extend(vect.renderers)
                
                tick += 1
                progress.setValue(tick)         
                
                if self.model.legend and vect.main:
                    # Create the legend for the main layer
                    self.writeLegendFile(uid, vect.renderers)  
                    
                tick += 1
                progress.setValue(tick)              
                  
            # Write symbol styles
            self.writeCss(uid, symbols, labels)  
            
            # Copy any external SVG files
            self.copyImgFiles(uid, symbols)
            
            # Alter the index file
            n = self.getDestIndexFile(uid)
            
            self.htmlWriter.writeIndexFile(n, self.model, bbox, labels)
            tick += 1
            progress.setValue(tick)
            
            ''''Order of things is important
            writeDataFile() appends an ID field if not already in the popup
            Would result in the popup template potentially having an unexpected ID field'''
            if self.model.popup == True or self.model.hasViz == True:
                self.__logger.info("EXPORT popup data")
                # Create the data files
                self.writeDataFile(uid) 
            
            # Now zip up the shapefiles
            self.zipShpFiles(uid)
            
            self.__logger.info("EXPORT complete =========================================================")
            
            tick += 1
            progress.setValue(tick)
                
            # start browser
            webbrowser.open_new_tab("{0}{1}/index.html".format(webServerUrl, uid))
   
    
    def getUniqueFolderName(self):  
        """Get a unique folder name"""
        return time.strftime("%Y%m%d%H%M%S")          
    
    def writeSymbology(self, layer, renderers):
        """Write the CSS value to the d3css column"""
        # Create a single transaction for the whole lot
        layer.startEditing() 
        # Loop through each symbol
        if renderers is not None:
            i = 0
            for r in renderers:
                filt = r.getFilterExpression((i == 0))
                self.__logger.info("Filter: " + filt)
                i += 1
                
                # Get the features with this particular symbology
                features = None
                if len(filt) > 0:
                    features = layer.getFeatures(QgsFeatureRequest().setFilterExpression(filt))
                else: 
                    features = layer.getFeatures()
                    
                # Loop though each feature returned from the filter
                for feature in features:
                    index = layer.fieldNameIndex(self.__colorField)                   
                    layer.changeAttributeValue(feature.id(), index, r.symbols[0].css)
                    index = layer.fieldNameIndex(self.__sizeField)                   
                    layer.changeAttributeValue(feature.id(), index, r.symbols[0].size)

            # Commit the transaction
            layer.commitChanges()
        
    def writeCss(self, uid, renderers, labels):
        """Create/append CSS file for symbology"""
        n = self.getDestCssFile(uid)
        f = open(n, "a")
        try:
            # write out the background color on the first iteration through the outer loop
            f.write(self.getCanvasStyle())
            
            # write out all the symbols associated with the layer
            if renderers is not None:
                for r in renderers:
                    f.write(r.symbols[0].toCss() + "\n")
                    
            # write out the label styles
            if labels is not None:
                for label in labels:
                    if label.hasLabels() == True:
                        f.write(label.getStyle() + "\n")
                        
        except Exception as e:
            # don't leave open files 
            self.__logger.error("Exception\r\n" + traceback.format_exc(None))
            raise e
        finally:
            f.close()
            
    def getCanvasStyle(self):
        """Get the canvas background color"""
        style = "#mapSvg{{background-color: {0};}}\n"
        return style.format(self.model.canvasBackground)
            
    def writeDataFile(self, uid):
        """Write the main info file which will be used in the popup"""
        main = self.model.getMainLayer()
        features = main.layer.getFeatures()
            
        n = self.getDestDataFile(uid)
        f = codecs.open(n, "a", "utf-8")
        try:
            if self.model.hasViz == True:
                # Merge the range data with any selected fields
                for range in self.model.ranges:
                    fields = range.getFields()
                    for field in fields:
                        if field not in self.model.selectedFields:
                            self.model.selectedFields.append(field)
            
            # Add the csv header
            if self.model.idField not in self.model.selectedFields:
                self.model.selectedFields.append(self.model.idField)
            
            f.write(u",".join(self.model.selectedFields))
            f.write("\n")  
              
            # Loop though each feature and read the values
            for feature in features:
                line = u""
                for field in self.model.selectedFields:
                    idField = (field == self.model.idField)
                    line += self.safeCsvString(feature[field], idField) + ","
                f.write(unicode(line[:-1]))
                f.write(u"\n")
            
        except Exception as e:
            self.__logger.error("Exception\r\n" + traceback.format_exc(None))
            raise e
        finally:
            f.close()
            
    def writeLegendFile(self, uid, renderers):
        """Write the legend for the main layer
        Output limited to Graduated and Categorized renderers"""
        
        '''Note: Only check the actual object, not derived types due to inheritance hierarchy'''
        if renderers is not None and len(renderers) > 0 and type(renderers[0]) != singleSymbol :
            n = self.getDestLegendFile(uid)
            f = codecs.open(n, "a", "utf-8")
            # for  now a fixed width and height for the legend
            template = u"{w},{h},{c},{t}\n"
            try:
                
                f.write("Width,Height,Color,Text\n");
                for r in renderers:
                    if len(r.label.strip()) > 0:
                        uCss = unicode(r.symbols[0].css)                    
                        uText = self.safeCsvUnicode(r.label, False)
                        
                        f.write(template.format(
                                                w=r.symbols[0].legendWidth,
                                                h=r.symbols[0].legendHeight,
                                                c=uCss,
                                                t=uText));
                        
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
                val = val[:len(val) - 2]        
            
        return val.replace(",", "")
        
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
                
        try:
            zipf = zipfile.ZipFile(os.path.join(path, dest), "w")
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f != dest:
                        filePath = os.path.join(root, f)
                        zipf.write(filePath, f)
                        os.remove(filePath)
            zipf.close()
        except:
            self.__logger.error2()
            pass
            
    def isWindows(self):
        """Windows OS?"""
        return self.osHelp.isWindows 
    
    def hasTopoJson(self):    
        """Does the system have node.js and topojson installed?""" 
    
        found = False
        
        try:   
            found = self.osHelp.helper.hasTopojson()
           
        except Exception:
            # What? log and continue
            self.__logger.error("Exception\r\n" + traceback.format_exc(None))

        return found      
            
    def getSourceFolder(self):
        """Get the plugin html source folder"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "html")
    
    def getDestFolder(self, uid):
        """Get the destination folder with the unique id appended"""
        safeFolder = self.model.outputFolder
        if self.isWindows() == True:
            safeFolder = self.model.outputFolder.encode('ascii', 'ignore')

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
    
    def getDestJsonFolder(self, uid):
        """Get the destination shapefile folder"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "json")
    
    def getDestImgFolder(self, uid):
        """Get the destination image file path"""
        folder = self.getDestFolder(uid)
        return os.path.join(folder, "img")
    
    def copyImgFiles(self, uid, renderers):
        """Copy any external image files for the layer symbology to the destination folder
        
        :param uid: Unique identifier for the destination folder 
        :type uid: string
        
        :param renderers: List of renderers associated with the layer symbology (categorised and graduated renederers will have more than one)
        :type renderers: list[d3MapRenderer.symbology.singleSymbol]
        
        """
        
        for r in renderers:
            for s in r.symbols:
                if s.hasImage() == True:
                    head, tail = os.path.split(s.path)
                    shutil.copyfile(s.path, os.path.join(self.getDestImgFolder(uid), tail))
        
    
    def addColumns(self, layer):
        """Add a new column to hold the color and size used in symbology"""
        if self.__qgis.hasField(layer, self.__colorField) == False:
            self.__qgis.addField(layer, self.__colorField) 
        if self.__qgis.hasField(layer, self.__sizeField) == False:
            self.__qgis.addField(layer, self.__sizeField)                                                
    
    def getProgressTicks(self):
        """Get the amount of progress steps"""
        layers = self.model.getLayersForOutput()
        return 3 + (6 * len(layers))
        
    def areLayersModified(self):
        """Have the chosen layers been modified?"""
        isEdit = False
        
        layers = self.model.getLayersForOutput()
        for vect in layers:    
            # TODO: Move these into separate attributes
            if vect.layer.isEditable() == True and vect.layer.isModified() == True:
                isEdit = True
                break
            
        return isEdit       
     
    
        
