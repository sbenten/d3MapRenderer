# coding=utf-8

from PyQt4.QtCore import QSettings
from qgis.core import *

class globalSettings(object):
    """Interact with the global QSettings class and QgsProject class"""
    
    def __init__(self):
        """Constructor. Create the settings objects"""
        self.s = QSettings()
        self.p = QgsProject.instance()
        
    def outputPath(self):
        outPath = self.p.readEntry("d3MapRenderer", "ProjOutputPath", u"")[0]
        
        if outPath == "":
            outPath = self.s.value("d3MapRenderer/OutputPath", u"")
        
        return  outPath         
        
    def webServerUrl(self):
        return self.s.value("d3MapRenderer/WebServerUrl", u"http://127.0.0.1:8080/")
        
    def outputFormat(self):
        return self.p.readEntry("d3MapRenderer", "OutputFormat", u"TopoJson")[0]
        
    def projection(self):
        return self.p.readEntry("d3MapRenderer", "d3Proj", u"")[0]
    
    def setOutputPath(self, val):
        if isinstance(val, unicode) == False:
            raise ValueError("Output path must be a text value")
        
        self.s.setValue("d3MapRenderer/OutputPath", val)
    
    def setWebServerUrl(self, val):
        if isinstance(val, unicode) == False:
            raise ValueError("Web server Url must be a text value")
        
        if val.endswith("/") == False:
            val = val + "/"
        
        self.s.setValue("d3MapRenderer/WebServerUrl", val)
    
    def setProjOutputPath(self, val):
        if isinstance(val, unicode) == False:
            raise ValueError("Project Output Path must be a text value")
        
        self.p.writeEntry("d3MapRenderer", "ProjOutputPath", val)
    
    def setOutputFormat(self, val):
        if isinstance(val, unicode) == False:
            raise ValueError("OutputFormat must be a text value")
        
        self.p.writeEntry("d3MapRenderer", "OutputFormat", val)
        
    def setProjection(self, val):
        if isinstance(val, unicode) == False:
            raise ValueError("Projection must be a text value")
        
        self.p.writeEntry("d3MapRenderer", "d3Proj", val)