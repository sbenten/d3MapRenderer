from qgis.core import *
from logger import log

class vector:
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
                
                
        renderer = layer.rendererV2()
        dump = renderer.dump()
        
        
        if dump[0:6] == "SINGLE":
            self.rendererType = 0            
        elif dump[0:11] == "CATEGORIZED":
            self.rendererType = 1        
        elif dump[0:9] == "GRADUATED":
            self.rendererType = 2
            
        """Log the parameters to the log messages panel"""
        template = u"""{name}
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
            
    def isSingleRenderer(self):
        """Is this a single renderer type?"""
        return self.rendererType == 0