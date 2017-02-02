import sys
import inspect
import traceback

from logger import log
from viz import *
from projections import *
from output import *
from symbology import *

class model(object):
    """Model for the UI
    Contains abstractions of all the chosen options for output to d3"""
    
    def __init__(self, backgroundColor):
        """Initialise the model"""
        self.__logger = log(self.__class__.__name__)
        
        self.__tempVizFields = [] 
        self.formats = []
        self.vectors = []   
        self.projections = [] 
        self.legendPositions = ["Top Left", "Top Right", "Bottom Right", "Bottom Left", "External"]
        self.popupPositions = ["Bubble", "External"]
        self.charts = [] 
        self.vizLabels = [] 
        self.osHelp = osHelper()
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
        
        
        self.title = u""
        self.showHeader = False
        self.width = 800
        self.height = 600
        self.idField = ""
        self.selectedFormat = None
        self.simplification = ""
        self.outputFolder = u""
        self.selectedProjection = None   
        self.legend = False              
        self.selectedLegendPosition = 0
        self.popup = False        
        self.selectedPopupPosition = 0
        self.panZoom = False
        self.extraVectors = False
        self.showLabels = False
        self.hasViz = False  
        self.selectedVizChart = None 
        self.vizWidth = 240
        self.vizHeight = 240  
        self.canvasBackground = backgroundColor 
        
                      
        self.selectedFields = [] 
        self.ranges = dataRanges() 
        
        # list of output formats
        frmts = [cls() for cls in supportedFormat.__subclasses__()]
        for f in frmts:
            self.formats.append(f)
            
        if len(self.formats) > 0:
            self.selectedFormat = self.formats[0]
        
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

        
    def logData(self):
        """Log the parameters to the log messages panel"""        
        template = u"       {0} = [{1}]"
        
        self.__logger.info(template.format("title", self.title))
        self.__logger.info(template.format("showHeader", str(self.showHeader)))
        self.__logger.info(template.format("width", str(self.width)))
        self.__logger.info(template.format("height", str(self.height)))
        self.__logger.info(template.format("idField", self.idField))     
        self.__logger.info(template.format("format", self.selectedFormat.name)) 
        self.__logger.info(template.format("simplification", self.simplification))
        self.__logger.info(template.format("outputFolder", self.outputFolder))
        self.__logger.info(template.format("selectedProjection", self.selectedProjection.name))
        self.__logger.info(template.format("popup", str(self.popup)))
        self.__logger.info(template.format("selectedPopupPosition", self.popupPositions[self.selectedPopupPosition]))
        self.__logger.info(template.format("popupTemplate", self.getPopupTemplate()))
        self.__logger.info(template.format("legend", str(self.legend)))
        self.__logger.info(template.format("selectedLegendPosition", self.legendPositions[self.selectedLegendPosition]))
        self.__logger.info(template.format("panZoom", str(self.panZoom)))
        self.__logger.info(template.format("extraVectors", str(self.extraVectors)))
        self.__logger.info(template.format("showLabels", str(self.showLabels)))
        self.__logger.info(template.format("hasViz", str(self.hasViz)))
        self.__logger.info(template.format("selectedVizChart", self.selectedVizChart.name))
        self.__logger.info(template.format("vizWidth", str(self.vizWidth)))
        self.__logger.info(template.format("vizHeight", str(self.vizHeight)))
        self.__logger.info(template.format("vizHeight", str(self.vizHeight)))
        self.__logger.info(template.format("vizDataRanges", self.getDataRangePreview()))  
        self.__logger.info(template.format("vizLabels", ", ".join(self.vizLabels))) 
        self.__logger.info(template.format("canvasBackground", str(self.canvasBackground)))       
        
        layers = self.getLayersForOutput()
        for l in layers:
            l.logData()

    
    def getLayersForOutput(self):
        """Get all the layers selected for output in the order defined in the QGIS legend"""
        found = []
        # Get all vector layers, extras as well as the main layer
        for v in self.vectors:
            if (self.extraVectors == True and v.extra == True) or v.main == True:
                found.append(v)
        # Reverse the order for processing the output, 
        # this will also form the order the SVG groups are created
        found.reverse()
        return found
       
    def setSelectedPopupField(self, name, state):
        """Set the selected field state"""
        if state == True:
            if name not in self.selectedFields:
                self.selectedFields.append(name)
        else:
            if name in self.selectedFields:
                self.selectedFields.remove(name)
                
    def setSelectedVizField(self, name, state):
        """Set the selected viz field state"""
        if state == True:
            if name not in self.__tempVizFields:
                self.__tempVizFields.append(name)
        else:
            if name in self.__tempVizFields:
                self.__tempVizFields.remove(name)
                
    def resetSelectedVizFields(self):
        """Reset the currently selected viz fields"""
        self.__tempVizFields[:] = []
                
    def getCurrentRangeLength(self):
        """Check the length of the current data range"""
        return len(self.__tempVizFields)
                
    def addCurrentRange(self, name):
        """Add the temporary data range to the list"""
        if len(self.__tempVizFields) > 0:
            data = dataRange(name)
            
            for f in self.__tempVizFields:
                data.appendField(f)
                
            self.ranges.append(data)
            self.resetSelectedVizFields()
            
            
    def getPopupTemplate(self):
        """Return the preview of the html popup"""
        return self.selectedFormat.getPopupTemplate(self.selectedFields, self.hasViz, self.vizWidth, self.vizHeight)
            
    def getDataRangePreview(self):
        """Get the preview of fields in each data range"""
        temp = ""
        
        for data in self.ranges:
            temp += data.getDisplayString()
            temp += "\r\n"
            
        return temp
        
    def deleteLastRange(self):
        """Remove the last data range from the list"""
        if len(self.ranges) > 0:
            self.ranges.pop()
            
    def resetRanges(self):
        """Remove all previously created ranges"""
        self.ranges[:] = []
        
    def getRangeCount(self):
        """Retrieve the count of data ranges"""
        return len(self.ranges)
        
    def getVizLabelMask(self):
        """Get the input mask for the data viz labels"""
        return self.ranges.getQtLabelMask()
            
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
            v.setMain(False)
        
        self.vectors[index].setMain(True)
        # also clear the list of selected fields
        self.selectedFields = []
        
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
    
    def isExternalTip(self):
        """Is the tooltip of data to be displayed outside the map?"""              
        return (self.selectedPopupPosition == 1)
    