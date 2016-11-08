# coding=utf-8

import math
import sys

class projection(object):
    """Base class for a projection object"""
    
    def __init__(self):

        self.name = ""
        self.d3Name = ""
        self.projection = ""
        self.safeCentroid = False

    def toScript(self, layer):
        """Base implementation"""
        return ""
    
    def getCenterX(self, bound):
        """Central position on the X Axis"""       
        return int(math.sqrt(math.pow(sum([bound.right, bound.left]), 2)))
    
    def getConicCenterX(self, bound):
        """Central position on the X Axis for Conic scripts"""
        left = float(math.sqrt(math.pow(bound.left, 2)))
        right = float(math.sqrt(math.pow(bound.right, 2)))
               
        return int(sum([right, left]) /2)
    
    def getCenterY(self, bound):
        """Central position on the Y Axis"""
        return int(sum([bound.top, bound.bottom]) / 2)
    
    def getBottomParallel(self, bound):
        """Bottom parallel"""
        return int(math.floor(bound.bottom))
    
    def getTopParallel(self, bound):
        """Bottom parallel"""
        return int(math.ceil(bound.top))
        
    def formatScript(self, bound, width, height):
        """Basic formatting for simple projections"""
        script = "{n}()\n      .center([{cx}, {cy}])\n      .scale(1000)\n      .translate([width / 2, height / 2])"
        
        output = script.format(
            n = self.d3Name,
            cx = self.getCenterX(bound),
            cy = self.getCenterY(bound))
        
        return output
        
    def formatConicScript(self, bound, width, height):
        """Basic formatting for conic projections"""
        script = "{n}()\n      .center([0, {cy}])\n      .rotate([{cx}, 0])\r\n      .parallels([{p1}, {p2}])\n      .scale(1000)\n      .translate([width / 2, height / 2])"
        
        output = script.format(
            n = self.d3Name,
            cx = self.getConicCenterX(bound),
            cy = self.getCenterY(bound),
            p1 = self.getBottomParallel(bound),
            p2 = self.getTopParallel(bound))
        
        return output
    
    def refineProjectionScript(self, mainObject):
        """Standard script to refine projections scale and translation on the client-side"""
        script =  """\n      // Refine projection
      var b, s, t;
      projection.scale(1).translate([0, 0]);
      var b = path.bounds({m});
      var s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
      var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];
      projection.scale(s).translate(t);\n"""
      
        return script.format(m = mainObject)
    
    def zoomBehaviourScript(self):
        """Standard zoom behaviour script"""
        return """    svg.call(d3.behavior.zoom()\n      .scaleExtent([1, 40])\n      .on("zoom", onZoom));"""
    
    def zoomScalingScript(self):
        """Create the JavaScript to re-scale the vectors"""
    
        return """vectors.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");\n"""  
    
        
""" TODO: Extra projections
# List of projections to support in the future...

d3.geo.armadillo()
d3.geo.azimuthalEqualArea()
d3.geo.azimuthalEquidistant()
d3.geo.berghaus()
d3.geo.bonne()
d3.geo.chamberlin()
d3.geo.craig()
d3.geo.cylindricalStereographic()
d3.geo.gilbert()
d3.geo.gingery()
d3.geo.gnomonic()
d3.geo.hammerRetroazimuthal()
d3.geo.littrow()
d3.geo.modifiedStereographic()
d3.geo.peirceQuincuncial()
d3.geo.polyhedron.butterfly()
d3.geo.polyhedron.waterman()
d3.geo.rectangularPolyconic()
d3.geo.satellite()
d3.geo.sinuMollweide()
d3.geo.stereographic()
d3.geo.twoPointAzimuthal()
d3.geo.twoPointEquidistant()
d3.geo.transverseMercator()
d3.geo.wiechel()

"""        
        
        
class aitoff(projection):
    
    def __init__(self):
        self.name = u"Aitoff"
        self.d3Name = u"d3.geo.aitoff"
        self.preview = "proj_aitoff.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
    
class albers(projection):
    
    def __init__(self):
        self.name = u"Albers"
        self.d3Name = u"d3.geo.albers"
        self.preview = "proj_albers.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
 
        return self.formatConicScript(bound, width, height)
        
class albersUsa(projection):

    def __init__(self):     
        self.name = u"Albers Usa"
        self.d3Name = u"d3.geo.albersUsa"
        self.preview = "proj_albersusa.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        script = "{n}()\n      .scale(1000)\n      .translate([width / 2, height / 2])"        
        return script.format(n = self.d3Name) 

class august(projection):

    def __init__(self):
        self.name = u"August"
        self.d3Name = u"d3.geo.august"
        self.preview = "proj_august.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class baker(projection):

    def __init__(self):
        self.name = u"Baker Dinomic"
        self.d3Name = u"d3.geo.baker"
        self.preview = "proj_baker.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
    
class boggs(projection):

    def __init__(self):
        self.name = u"Boggs Eumorphic"
        self.d3Name = u"d3.geo.boggs"
        self.preview = "proj_boggs.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class bromley(projection):
    
    def __init__(self):
        self.name = u"Bromley"
        self.d3Name = u"d3.geo.bromley"
        self.preview = "proj_bromley.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class collignon(projection):

    def __init__(self):
        self.name = u"Collignon"
        self.d3Name = u"d3.geo.collignon"
        self.preview = "proj_collignon.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
        
class conicEquidistant(projection):

    def __init__(self):
        self.name = u"Conic Equi-distant"
        self.d3Name = u"d3.geo.conicEquidistant"
        self.preview = "proj_conicequidistant.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class craster(projection):

    def __init__(self):
        self.name = u"Craster Parabolic"
        self.d3Name = u"d3.geo.craster"
        self.preview = "proj_craster.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
 
        return self.formatScript(bound, width, height) 
    
class cylindricalEqualArea(projection):
    
    def __init__(self):
        self.name = u"Cylindrical Equal Area"
        self.d3Name = u"d3.geo.cylindricalEqualArea"
        self.preview = "proj_cylindrical.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height)   
  
class eckert1(projection):

    def __init__(self):
        self.name = u"Eckert I"
        self.d3Name = u"d3.geo.eckert1"
        self.preview = "proj_eckert1.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height)
    
class eckert2(projection):

    def __init__(self):
        self.name = u"Eckert II"
        self.d3Name = u"d3.geo.eckert2"
        self.preview = "proj_eckert2.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height)     
    
class eckert3(projection):

    def __init__(self):

        self.name = u"Eckert III"
        self.d3Name = u"d3.geo.eckert3"
        self.preview = "proj_eckert3.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
 
        return self.formatScript(bound, width, height)
    
        
class eckert4(projection):
    
    def __init__(self):
        self.name = u"Eckert IV"
        self.d3Name = u"d3.geo.eckert4"
        self.preview = "proj_eckert4.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
    
class eckert5(projection):
    
    def __init__(self):
        self.name = u"Eckert V"
        self.d3Name = u"d3.geo.eckert5"
        self.preview = "proj_eckert5.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
        
class eckert6(projection):
    
    def __init__(self):
        self.name = u"Eckert VI"
        self.d3Name = u"d3.geo.eckert6"
        self.preview = "proj_eckert6.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)

class eisenlohr(projection):
    
    def __init__(self):
        self.name = u"Eisenlohr"
        self.d3Name = u"d3.geo.eisenlohr"
        self.preview = "proj_eisenlohr.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class equirectangular(projection):

    def __init__(self):
        self.name = u"Equi Rectangular (Plate Carrée)"
        self.d3Name = u"d3.geo.equirectangular"
        self.preview = "proj_equirectangular.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
        
class fahey(projection):
    
    def __init__(self):
        self.name = u"Fahey"
        self.d3Name = u"d3.geo.fahey"
        self.preview = "proj_fahey.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class mtFlatPolarParabolic(projection):
    
    def __init__(self):
        self.name = u"Flat-Polar Parabolic"
        self.d3Name = u"d3.geo.mtFlatPolarParabolic"
        self.preview = "proj_flatpolarp.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class mtFlatPolarQuartic(projection):
    
    def __init__(self):
        self.name = u"Flat-Polar Quartic"
        self.d3Name = u"d3.geo.mtFlatPolarQuartic"
        self.preview = "proj_flatpolarq.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class mtFlatPolarSinusoidal(projection):
    
    def __init__(self):
        self.name = u"Flat-Polar Sinusoidal"
        self.d3Name = u"d3.geo.mtFlatPolarSinusoidal"
        self.preview = "proj_flatpolars.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class ginzburg4(projection):
    
    def __init__(self):
        self.name = u"Ginzburg IV"
        self.d3Name = u"d3.geo.ginzburg4"
        self.preview = "proj_ginzburg4.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class ginzburg5(projection):
    
    def __init__(self):
        self.name = u"Ginzburg V"
        self.d3Name = u"d3.geo.ginzburg5"
        self.preview = "proj_ginzburg5.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class ginzburg6(projection):

    
    def __init__(self):
        self.name = u"Ginzburg VI"
        self.d3Name = u"d3.geo.ginzburg6"
        self.preview = "proj_ginzburg6.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class ginzburg8(projection):

    def __init__(self):
        self.name = u"Ginzburg VIII"
        self.d3Name = u"d3.geo.ginzburg8"
        self.preview = "proj_ginzburg8.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class ginzburg9(projection):
    
    def __init__(self):
        self.name = u"Ginzburg IX"
        self.d3Name = u"d3.geo.ginzburg9"
        self.preview = "proj_ginzburg9.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class homolosine(projection):
    
    def __init__(self):
        self.name = u"Goode Homolosine"
        self.d3Name = u"d3.geo.homolosine"
        self.preview = "proj_goode.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
 
class gringorten(projection):
    
    def __init__(self):
        self.name = u"Gringorten Equal-Area"
        self.d3Name = u"d3.geo.gringorten"
        self.preview = "proj_gringorten.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class guyou(projection):
    
    def __init__(self):
        self.name = u"Guyou"
        self.d3Name = u"d3.geo.guyou"
        self.preview = "proj_guyou.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class hammer(projection):
    
    def __init__(self):
        self.name = u"Hammer"
        self.d3Name = u"d3.geo.hammer"
        self.preview = "proj_hammer.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class healpix(projection):
    
    def __init__(self):
        self.name = u"HEALPix"
        self.d3Name = u"d3.geo.healpix"
        self.preview = "proj_healpix.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class hill(projection):

    def __init__(self):
        self.name = u"Hill Eucyclic"
        self.d3Name = u"d3.geo.hill"
        self.preview = "proj_hill.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class kavrayskiy7(projection):
    
    def __init__(self):
        self.name = u"Kavrayskiy VII"
        self.d3Name = u"d3.geo.kavrayskiy7"
        self.preview = "proj_kavrayskiy7.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class lagrange(projection):
    
    def __init__(self):
        self.name = u"Lagrange"
        self.d3Name = u"d3.geo.lagrange"
        self.preview = "proj_lagrange.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
    
class conicConformal(projection):
    
    def __init__(self):
        self.name = u"Lambert Conic Conformal"
        self.d3Name = u"d3.geo.conicConformal"
        self.preview = "proj_lambert.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatConicScript(bound, width, height) 

class larrivee(projection):

    def __init__(self):
        self.name = u"Larrivée"
        self.d3Name = u"d3.geo.larrivee"
        self.preview = "proj_larrivee.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class laskowski(projection):

    def __init__(self):
        self.name = u"Laskowski Tri-Optimal"
        self.d3Name = u"d3.geo.laskowski"
        self.preview = "proj_laskowski.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
        
class loximuthal(projection):
    
    def __init__(self):
        self.name = u"Loximuthal"
        self.d3Name = u"d3.geo.loximuthal"
        self.preview = "proj_loximuthal.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)         
        
class mercator(projection):
    
    def __init__(self):
        self.name = u"Mercator"
        self.d3Name = u"d3.geo.mercator"
        self.preview = "proj_mercator.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)  
    
class miller(projection):
    """Miller projection"""
    
    def __init__(self):
        self.name = u"Miller"
        self.d3Name = u"d3.geo.miller"
        self.preview = "proj_miller.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class mollweide(projection):
    
    def __init__(self):
        self.name = u"Mollweide"
        self.d3Name = u"d3.geo.mollweide"
        self.preview = "proj_mollweide.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class naturalEarth(projection):
    
    def __init__(self):
        self.name = u"Natural Earth"
        self.d3Name = u"d3.geo.naturalEarth"
        self.preview = "proj_naturalearth.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class nellHammer(projection):

    def __init__(self):
        self.name = u"Nell–Hammer"
        self.d3Name = u"d3.geo.nellHammer"
        self.preview = "proj_nellhammer.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class orthographic(projection):

    def __init__(self):
        self.name = u"Orthographic"
        self.d3Name = u"d3.geo.orthographic"
        self.preview = "proj_orthographic.png"
        self.safeCentroid = True
        
    def toScript(self, bound, width, height): 
        
        script = "{n}()\n      .scale({s})\n      .translate([{tx}, {ty}])\n      .clipAngle(90)\n      .rotate([{cx}, {cy}])"
        
        scale = self.getScale(width, height)
        transX = self.getTransform(scale, width)
        transY = self.getTransform(scale, height)
        
        output = script.format(
            n = self.d3Name,
            cx = self.getCenterX(bound),
            cy = self.getCenterY(bound),
            s = scale,
            tx = transX,
            ty = transY)

        return output 
    
    def getCenterX(self, bound):
        """Central position on the X Axis for Conic scripts"""
        left = float(math.sqrt(math.pow(bound.left, 2)))
        right = float(math.sqrt(math.pow(bound.right, 2)))
              
        val = int(sum([right, left]) /2)
               
        if bound.left > 0:
            val = -val       
            
        if str(bound.left) == "-180.0" and str(bound.right) == "180.0":
            val = 0.0
        
        return val
    
    def getCenterY(self, bound):
        """Central position on the Y Axis"""
        return -int(sum([bound.top, bound.bottom]) / 2)

    def getScale(self, width, height):
        """Get the orthographic scale for the FULL globe"""
        return 0.95 / max((1.99 / width), (1.99 / height))
    
    def getTransform(self, scale, axis):
        """Get the transformation for the axis for the FULL globe"""
        return axis - scale     
    
    def refineProjectionScript(self, mainObject):
        """Orthographic projection relies on the FULL globe, not just a particular layer"""
        return ""
    
    def zoomBehaviourScript(self):
        """Orthographic projections use d3.geo.zoom"""
        return """    svg.call(d3.geo.zoom().projection(projection).on("zoom", onZoom))"""
    
    def zoomScalingScript(self):
        """Orthographic version of the scaling script"""
        return """svg.selectAll("path").attr("d", path);\n"""

class patterson(projection):

    def __init__(self):
        self.name = u"Patterson Cylindrical"
        self.d3Name = u"d3.geo.patterson"
        self.preview = "proj_patterson.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class polyconic(projection):

    def __init__(self):
        self.name = u"Polyconic"
        self.d3Name = u"d3.geo.polyconic"
        self.preview = "proj_polyconic.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class robinson(projection):

    def __init__(self):
        self.name = u"Robinson"
        self.d3Name = u"d3.geo.robinson"
        self.preview = "proj_robinson.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
'''class satellite(projection):

    def __init__(self):
        self.name = u"Satellite"
        self.d3Name = u"d3.geo.satellite"
        self.preview = "proj_robinson.png"
        
    def toScript(self, bound, width, height): 
    
        distance = 1.1    
        script = """{n}()    
    .distance({d})
    .scale({s})
    .rotate([{cx}, {cy}, 0])
    .center([{cx}, {cy}])
    .tilt(25)
    .clipAngle(Math.acos(1 / {d}) * 180 / Math.PI - 1e-6)
    .precision(.1)"""
        
        scale = self.getScale(width, height)
        
        output = script.format(
            n = self.d3Name,
            d = distance,
            cx = self.getCenterX(bound),
            cy = self.getCenterY(bound),
            s = scale)

        return output 
    
    def getCenterX(self, bound):
        """Central position on the X Axis for Conic scripts"""
        left = float(math.sqrt(math.pow(bound.left, 2)))
        right = float(math.sqrt(math.pow(bound.right, 2)))
              
        val = int(sum([right, left]) /2)
               
        if bound.left > 0:
            val = -val       
            
        if str(bound.left) == "-180.0" and str(bound.right) == "180.0":
            val = 0.0
        
        return val
    
    def getCenterY(self, bound):
        """Central position on the Y Axis"""
        return -int(sum([bound.top, bound.bottom]) / 2)

    def getScale(self, width, height):
        """Get the orthographic scale for the FULL globe"""
        return 0.95 / max((1.99 / width), (1.99 / height))   
    
    def refineProjectionScript(self, mainObject):
        """Orthographic projection relies on the FULL globe, not just a particular layer"""
        return ""
    
    def zoomBehaviourScript(self):
        """Orthographic projections use d3.geo.zoom"""
        return """    svg.call(d3.geo.zoom().projection(projection).on("zoom", onZoom))"""
    
    def zoomScalingScript(self, outputLayers):
        """Orthographic version of the scaling script"""
        return """svg.selectAll("path").attr("d", path);"""'''
    
class sinusoidal(projection):
    
    def __init__(self):
        self.name = u"Sinusoidal"
        self.d3Name = u"d3.geo.sinusoidal"
        self.preview = "proj_sinusoidal.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class times(projection):
    
    def __init__(self):
        self.name = u"Times"
        self.d3Name = u"d3.geo.times"
        self.preview = "proj_times.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class vanDerGrinten(projection):
 
    def __init__(self):
        self.name = u"Van der Grinten I"
        self.d3Name = u"d3.geo.vanDerGrinten"
        self.preview = "proj_vandergrinten.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class vanDerGrinten2(projection):

    def __init__(self):
        self.name = u"Van der Grinten II"
        self.d3Name = u"d3.geo.vanDerGrinten2"
        self.preview = "proj_vandergrinten2.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class vanDerGrinten3(projection):

    def __init__(self):
        self.name = u"Van der Grinten III"
        self.d3Name = u"d3.geo.vanDerGrinten3"
        self.preview = "proj_vandergrinten3.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class vanDerGrinten4(projection):
    
    def __init__(self):
        self.name = u"Van der Grinten IV"
        self.d3Name = u"d3.geo.vanDerGrinten4"
        self.preview = "proj_vandergrinten4.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class wagner4(projection):

    def __init__(self):
        self.name = u"Wagner IV"
        self.d3Name = u"d3.geo.wagner4"
        self.preview = "proj_wagner4.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class wagner6(projection):
    
    def __init__(self):
        self.name = u"Wagner VI"
        self.d3Name = u"d3.geo.wagner6"
        self.preview = "proj_wagner6.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class wagner7(projection):    
    def __init__(self):
        self.name = u"Wagner VII"
        self.d3Name = u"d3.geo.wagner7"
        self.preview = "proj_wagner7.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class winkelTripel(projection):

    def __init__(self):
        self.name = u"Winkel Tripel"
        self.d3Name = u"d3.geo.winkel3"
        self.preview = "proj_winkel3.png"
        self.safeCentroid = False
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 