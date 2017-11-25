import re
from qgis.core import *
from logger import log
from symbology import *

class vector(object):
    """Base class for the layer abstracting away the QGIS details"""
    
    def __init__(self, iface, layer):
        """Initialise the layer"""
        self.__logger = log(self.__class__.__name__)
        
        self.rendererType = 0
        self.id = layer.id()
        self.name = layer.name()
        self.layer = layer
        self.filePath = ""
        self.main = False
        self.extra = iface.legendInterface().isLayerVisible(layer)
        self.type = layer.type()
        self.fields = []
        self.vizFields = []
        self.defaultId = "" 
        
        self.hasTip = False
        self.hasViz = False 
              
        self.renderers = renderers()  
        """A list of renderers, representing each class in the data range"""
        
        self.averageOutlineWidth = 1
        
        self.isVisible = iface.legendInterface().isLayerVisible(layer) 
        self.transparency = 1 - (float(layer.layerTransparency()) / 100)
        
        for f in layer.pendingFields():
            # Add to the list of fields
            self.fields.append(f.name()) 
            
            # Add numeric fields to the list for visualization
            if f.typeName().lower() == "integer" or f.typeName().lower() == "real" or f.typeName().lower() == "integer64":
                self.vizFields.append(f.name())
            
            # An ID field? Set the default for the ID field option    
            upper = f.name().upper() 
            if upper == "ID" or upper == "OBJECT_ID" or upper == "OBJECTID":
                self.defaultId = f.name()
        
        # Now read the symbology for the layer
        self.getSymbology(layer)   
        
    def setMain(self, state):     
        """Set whether the vector layer is the main layer"""
        self.main = state
        for r in self.renderers:
            for s in r.symbols:
                s.isMain = state
                
    def setOutputOrder(self, outIndex):
        """Assign the output order of the layer, so that the various CSS and JavaSripts have the right IDs"""
        cssstub = self.getLayerObjectName(outIndex)          
        for i, r in enumerate(self.renderers):
            r.setOutputCss(i, u"{0}c{1}".format(cssstub, str(i)))

    
    def getSafeName(self):
        """Return a string condsidered safe for use in file names"""
        pattern = re.compile('[\W_]+', re.UNICODE)
        return pattern.sub("", self.name) 

    def getLayerObjectName(self, outIndex):
        """Get a unique layer name as an object within topojson"""
        stub = u"l{0}"
        
        return stub.format(str(outIndex))            
            
    def getSymbology(self, layer):
        """Read the symbology, generate a CSS style and set against each row in the layers attribute table"""       
        renderer = layer.rendererV2()
        dump = renderer.dump()
        
        if dump[0:6] == "SINGLE":
            self.getSingleSymbol(layer, renderer, self.transparency)             
        elif dump[0:11] == "CATEGORIZED":                 
            self.getCategorizedSymbol(layer, renderer, self.transparency)    
        elif dump[0:9] == "GRADUATED":
            self.getGraduatedSymbol(layer, renderer, self.transparency)
        else:
            words = dump.split(" ")
            self.__logger.error("{0} renderer in {1} not supported".format(words[0], layer.name))
            # Unknown type, fall back onto the single renderer
            self.getSingleSymbol(layer, renderer, self.transparency) 
            
    
    def getSingleSymbol(self, layer, renderer, transparency):
        """Read the symbology for single symbol layers"""      
        geoType = layer.geometryType()       
        
        self.rendererType = 0 
        s = singleSymbol(geoType, renderer.symbol(), transparency) 
        self.renderers.append(s)       
            
    def getCategorizedSymbol(self, layer, renderer, transparency):
        """Read the symbology for categorized symbol layers"""        
        field = renderer.classAttribute()
        geoType = layer.geometryType()

        self.rendererType = 1
        
        fieldType = "String"
        fields = layer.pendingFields()
        for f in fields:
            if f.name() == field:
                fieldType = f.typeName()    
                break
        
        for c in renderer.categories():
            s = categorized(geoType, field, fieldType, c, transparency)     
            self.renderers.append(s)
            
                            
    def getGraduatedSymbol(self, layer, renderer, transparency):
        """Read the symbology for graduated symbol layers"""
        field = renderer.classAttribute()
        geoType = layer.geometryType()

        self.rendererType = 2
                    
        for r in renderer.ranges():
            s = graduated(geoType, field, r, transparency)     
            self.renderers.append(s)
    
    
    def logData(self):
        """Log the parameters to the log messages panel"""

        template = u"""       {name}
       id = [{id}]
       type = [{type}]
       renderer = [{renderer}]
       extra = [{extra}]
       colid = [{colid}]
       visible = [{visible}]
       trans = [{trans}]"""
        
        self.__logger.info(template.format(
            name = self.name,
            id = self.id,
            type = self.type,
            renderer = self.rendererType,
            extra = self.extra,
            colid = self.defaultId,
            visible = self.isVisible,
            trans = self.transparency
        ))
        
        # Now call the symbology logger
        self.renderers.logData()
            
    def isSingleRenderer(self):
        """Is this a single renderer type?"""
        return self.rendererType == 0