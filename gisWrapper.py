from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PyQt4.QtCore import *

from logger import log

class qgisWrapper(object):

    def __init__(self):
        """Constructor"""
        self.__logger = log(self.__class__.__name__)        
        
    def openShape(self, filePath, objName):
        """Open a shapefile as a QgisVectorLayer"""
        return QgsVectorLayer(filePath, objName, "ogr")
        
    def saveShape(self, qgisLayer, filePath):
        """Save the shapefile in WGS84 with new color column"""       
        crs = self.getDefaultCrs()
        QgsVectorFileWriter.writeAsVectorFormat(qgisLayer,
                                                filePath,
                                                "system",
                                                crs,
                                                "ESRI Shapefile")
                                  
    def getDefaultCrs(self):
        """Get the default CRS for geojson and topojson"""
        
        return QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)  
    
    def addField(self, qgisLayer, name):
        """Add a new column to the layer data provider with the given name"""
        self.__logger.info("Adding field: " + name)
        
        qgisLayer.startEditing()
        
        provider = qgisLayer.dataProvider()
        provider.addAttributes([ QgsField(name, QVariant.String) ])
        
        qgisLayer.commitChanges()
            
    def hasField(self, qgisLayer, name):
        """Does a particular field already exist?"""
        result = False
        
        if qgisLayer.fieldNameIndex(name) > -1:
            result = True
        
        return result  
    
    def removeFields(self, qgisLayer, preserveNames):
        """Remove all fields but those in the preserve list"""
        qgisLayer.startEditing()
        
        provider = qgisLayer.dataProvider()
        
        fields = provider.fields()
        delIndicies = list()

        index = 0
        for field in fields:
            if field.name() not in preserveNames:
                delIndicies.append(index)
            index += 1
        
        provider.deleteAttributes(delIndicies)
        
        qgisLayer.commitChanges()