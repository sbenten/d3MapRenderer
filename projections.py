import math
import sys
current_module = sys.modules[__name__]

from logger import log
from bbox import bound

class projection(object):
    """Base class for a projection object"""
    
    def __init__(self):
        """Constructor"""
        self.name = ""
        self.projection = ""

    def toScript(self, layer):
        """Base implementation"""
        return ""
    
    def getCenterX(self, bound):
        """Central position on the X Axis"""
        return int(sum([bound.right, bound.left]) /2)
    
    def getCenterY(self, bound):
        """Central position on the Y Axis"""
        return int(sum([bound.top, bound.bottom]) / 2)
    
    def getBottomParallel(self, bound):
        """Bottom parallel"""
        return int(math.floor(bound.bottom))
    
    def getTopParallel(self, bound):
        """Bottom parallel"""
        return int(math.ceil(bound.top))
    
    '''def getScale(self, bound, width, height):
        """Scale to 95% of the longest axis"""
        return .95 / max((bound.right - bound.left) / width, (bound.top - bound.bottom) / height)
    
    def getTranslationX(self, bound, width, scale):
        """Translate by finding the center and and muliplying by the scale"""
        return (width - scale * (bound.right + bound.left)) / 2
    
    def getTranslationY(self, bound, height, scale):
        """Translate by finding the center and and muliplying by the scale"""
        return (height - scale * (bound.top + bound.bottom)) / 2'''
    
    def formatScript(self, d3Name, bound, width, height):
        """Basic formatting for simple projections"""
        script = "{n}()\n      .center([{cx}, {cy}])\n      .scale(1000)\n      .translate([width / 2, height / 2])"
        
        output = script.format(
            n = d3Name,
            cx = self.getCenterX(bound),
            cy = self.getCenterY(bound))
        
        return output
        
    def formatConicScript(self, d3Name, bound, width, height):
        """Basic formatting for conic projections"""
        script = "{n}()\n      .center([0, {cy}])\n      .rotate([{cx}, 0])\r\n      .parallels([{p1}, {p2}])\n      .scale(1000)\n      .translate([width / 2, height / 2])"
        
        output = script.format(
            n = d3Name,
            cx = math.sqrt(math.pow(self.getCenterX(bound), 2)),
            cy = self.getCenterY(bound),
            p1 = self.getBottomParallel(bound),
            p2 = self.getTopParallel(bound))
        
        return output
        
    
class albers(projection):
    """Albers projection"""
    
    def __init__(self):
        """Constructor"""
        
        self.name = "Albers"
        self.__d3Name = "d3.geo.albers"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatConicScript(self.__d3Name, bound, width, height)
        
class albersUsa(projection):
    """Albers projection"""
    
    def __init__(self):
        """Constructor"""        
        self.name = "Albers Usa"
        self.__d3Name = "d3.geo.albersUsa"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        script = "{n}()\n      .scale(1000)\n      .translate([width / 2, height / 2])"
        
        return script.format(n = self.__d3Name)
    
class conicConformal(projection):
    """Conic Equal Area projection"""
    
    def __init__(self):
        self.name = "Conic Conformal"
        self.__d3Name = "d3.geo.conicConformal"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatConicScript(self.__d3Name, bound, width, height)  

class conicEquidistant(projection):
    """Conic Equi-distant Projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Conic Equi-distant"
        self.__d3Name = "d3.geo.conicEquidistant"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class cylindricalEqualArea(projection):
    """Cylindrical Equal Area"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Cylindrical Equal Area"
        self.__d3Name = "d3.geo.cylindricalEqualArea"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class equirectangular(projection):
    """Equi Rectangular projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Equi Rectangular"
        self.__d3Name = "d3.geo.equirectangular"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)        
  
class eckert1(projection):
    """Eckert I projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Eckert I"
        self.__d3Name = "d3.geo.eckert1"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
    
class eckert2(projection):
    """Eckert II projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Eckert II"
        self.__d3Name = "d3.geo.eckert2"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)     
    
class eckert3(projection):
    """Eckert III projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Eckert III"
        self.__d3Name = "d3.geo.eckert3"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
    
        
class eckert4(projection):
    """Eckert IV projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Eckert IV"
        self.__d3Name = "d3.geo.eckert4"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
    
    
class eckert5(projection):
    """Eckert V projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Eckert V"
        self.__d3Name = "d3.geo.eckert5"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
    
        
class eckert6(projection):
    """Eckert VI projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Eckert VI"
        self.__d3Name = "d3.geo.eckert6"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
    
class fahey(projection):
    """Fahey projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Fahey"
        self.__d3Name = "d3.geo.fahey"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
 
class gringorten(projection):
    """Gringorten Equal-Area"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Gringorten Equal-Area"
        self.__d3Name = "d3.geo.gringorten"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 

class hammer(projection):
    """Hammer projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Hammer"
        self.__d3Name = "d3.geo.hammer"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 

class hill(projection):
    """Hill Eucyclic"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Hill"
        self.__d3Name = "d3.geo.hill"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
        
class mercator(projection):
    """Mercator projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Mercator"
        self.__d3Name = "d3.geo.mercator"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)  
    
class miller(projection):
    """Miller projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Miller"
        self.__d3Name = "d3.geo.miller"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 

class mollweide(projection):
    """Mollweide projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Mollweide"
        self.__d3Name = "d3.geo.mollweide"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 

class naturalEarth(projection):
    """Natural Earth projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Natural Earth"
        self.__d3Name = "d3.geo.naturalEarth"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class robinson(projection):
    """Robinson projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Robinson"
        self.__d3Name = "d3.geo.robinson"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height)
    
class sinusoidal(projection):
    """Sinusoidal projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Sinusoidal"
        self.__d3Name = "d3.geo.sinusoidal"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class wagner4(projection):
    """Wagner IV projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Wagner IV"
        self.__d3Name = "d3.geo.wagner4"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class wagner6(projection):
    """Wagner VI projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Wagner VI"
        self.__d3Name = "d3.geo.wagner6"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class wagner7(projection):
    """Wagner VII projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Wagner VII"
        self.__d3Name = "d3.geo.wagner7"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 
    
class winkelTripel(projection):
    """Winkel Tripel projection"""
    
    def __init__(self):
        """Constructor"""
        self.name = "Winkel Tripel"
        self.__d3Name = "d3.geo.winkel3"
        
    def toScript(self, bound, width, height):
        """Get the d3 JavaScript code required for the projection"""
        return self.formatScript(self.__d3Name, bound, width, height) 