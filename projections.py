# coding=utf-8

import math
import sys

class projection(object):
    """Base class for a projection object"""
    
    def __init__(self):

        self.name = ""
        self.d3Name = ""
        self.projection = ""

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
    
    def zoomBehaviourScript(self):
        """Standard zoom behaviour script"""
        return """    svg.call(d3.behavior.zoom()\n      .scaleExtent([1, 40])\n      .on("zoom", onZoom));"""
    
    def zoomScalingScript(self, outputLayers):
        """Create the JavaScript to re-scale the vectors"""
        
        scripts = []
        scripts.append("""vectors.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");\n""")
        
        template = "      vector{index}.style(\"stroke-width\", {width} / d3.event.scale);\n"
        
        for i, o in enumerate(outputLayers):
            if o.strokeWidth > 0:
                script = template.format(
                    index = i,
                    width = o.strokeWidth
                )
                scripts.append(script)
    
        return "".join(scripts)  
    
    def dragBehaviourScript(self):
        """Default drag behaviour script"""
        
        return ""
        
class aitoff(projection):
    
    def __init__(self):
        self.name = u"Aitoff"
        self.d3Name = u"d3.geo.aitoff"
        self.preview = "proj_aitoff.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
    
class albers(projection):
    
    def __init__(self):
        self.name = u"Albers"
        self.d3Name = u"d3.geo.albers"
        self.preview = "proj_albers.png"
        
    def toScript(self, bound, width, height):
 
        return self.formatConicScript(bound, width, height)
        
class albersUsa(projection):

    def __init__(self):     
        self.name = u"Albers Usa"
        self.d3Name = u"d3.geo.albersUsa"
        self.preview = "proj_albersusa.png"
        
    def toScript(self, bound, width, height): 
        script = "{n}()\n      .scale(1000)\n      .translate([width / 2, height / 2])"        
        return script.format(n = self.d3Name) 

class august(projection):

    def __init__(self):
        self.name = u"August"
        self.d3Name = u"d3.geo.august"
        self.preview = "proj_august.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class baker(projection):

    def __init__(self):
        self.name = u"Baker Dinomic"
        self.d3Name = u"d3.geo.baker"
        self.preview = "proj_baker.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
    
class boggs(projection):

    def __init__(self):
        self.name = u"Boggs Eumorphic"
        self.d3Name = u"d3.geo.boggs"
        self.preview = "proj_boggs.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class bromley(projection):
    
    def __init__(self):
        self.name = u"Bromley"
        self.d3Name = u"d3.geo.bromley"
        self.preview = "proj_bromley.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class collignon(projection):

    def __init__(self):
        self.name = u"Collignon"
        self.d3Name = u"d3.geo.collignon"
        self.preview = "proj_collignon.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
        
class conicEquidistant(projection):

    def __init__(self):
        self.name = u"Conic Equi-distant"
        self.d3Name = u"d3.geo.conicEquidistant"
        self.preview = "proj_conicequidistant.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class craster(projection):

    def __init__(self):
        self.name = u"Craster Parabolic"
        self.d3Name = u"d3.geo.craster"
        self.preview = "proj_craster.png"
        
    def toScript(self, bound, width, height):
 
        return self.formatScript(bound, width, height) 
    
class cylindricalEqualArea(projection):
    
    def __init__(self):
        self.name = u"Cylindrical Equal Area"
        self.d3Name = u"d3.geo.cylindricalEqualArea"
        self.preview = "proj_cylindrical.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height)   
  
class eckert1(projection):

    def __init__(self):
        self.name = u"Eckert I"
        self.d3Name = u"d3.geo.eckert1"
        self.preview = "proj_eckert1.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height)
    
class eckert2(projection):

    def __init__(self):
        self.name = u"Eckert II"
        self.d3Name = u"d3.geo.eckert2"
        self.preview = "proj_eckert2.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height)     
    
class eckert3(projection):

    def __init__(self):

        self.name = u"Eckert III"
        self.d3Name = u"d3.geo.eckert3"
        self.preview = "proj_eckert3.png"
        
    def toScript(self, bound, width, height):
 
        return self.formatScript(bound, width, height)
    
        
class eckert4(projection):
    
    def __init__(self):
        self.name = u"Eckert IV"
        self.d3Name = u"d3.geo.eckert4"
        self.preview = "proj_eckert4.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
    
class eckert5(projection):
    
    def __init__(self):
        self.name = u"Eckert V"
        self.d3Name = u"d3.geo.eckert5"
        self.preview = "proj_eckert5.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
        
class eckert6(projection):
    
    def __init__(self):
        self.name = u"Eckert VI"
        self.d3Name = u"d3.geo.eckert6"
        self.preview = "proj_eckert6.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)

class eisenlohr(projection):
    
    def __init__(self):
        self.name = u"Eisenlohr"
        self.d3Name = u"d3.geo.eisenlohr"
        self.preview = "proj_eisenlohr.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class equirectangular(projection):

    def __init__(self):
        self.name = u"Equi Rectangular (Plate Carrée)"
        self.d3Name = u"d3.geo.equirectangular"
        self.preview = "proj_equirectangular.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
        
class fahey(projection):
    
    def __init__(self):
        self.name = u"Fahey"
        self.d3Name = u"d3.geo.fahey"
        self.preview = "proj_fahey.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class mtFlatPolarParabolic(projection):
    
    def __init__(self):
        self.name = u"Flat-Polar Parabolic"
        self.d3Name = u"d3.geo.mtFlatPolarParabolic"
        self.preview = "proj_flatpolarp.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class mtFlatPolarQuartic(projection):
    
    def __init__(self):
        self.name = u"Flat-Polar Quartic"
        self.d3Name = u"d3.geo.mtFlatPolarQuartic"
        self.preview = "proj_flatpolarq.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class mtFlatPolarSinusoidal(projection):
    
    def __init__(self):
        self.name = u"Flat-Polar Sinusoidal"
        self.d3Name = u"d3.geo.mtFlatPolarSinusoidal"
        self.preview = "proj_flatpolars.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class ginzburg4(projection):
    
    def __init__(self):
        self.name = u"Ginzburg IV"
        self.d3Name = u"d3.geo.ginzburg4"
        self.preview = "proj_ginzburg4.png"
        
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
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class ginzburg8(projection):

    def __init__(self):
        self.name = u"Ginzburg VIII"
        self.d3Name = u"d3.geo.ginzburg8"
        self.preview = "proj_ginzburg8.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class ginzburg9(projection):
    
    def __init__(self):
        self.name = u"Ginzburg IX"
        self.d3Name = u"d3.geo.ginzburg9"
        self.preview = "proj_ginzburg9.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class homolosine(projection):
    
    def __init__(self):
        self.name = u"Goode Homolosine"
        self.d3Name = u"d3.geo.homolosine"
        self.preview = "proj_goode.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
 
class gringorten(projection):
    
    def __init__(self):
        self.name = u"Gringorten Equal-Area"
        self.d3Name = u"d3.geo.gringorten"
        self.preview = "proj_gringorten.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class guyou(projection):
    
    def __init__(self):
        self.name = u"Guyou"
        self.d3Name = u"d3.geo.guyou"
        self.preview = "proj_guyou.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class hammer(projection):
    
    def __init__(self):
        self.name = u"Hammer"
        self.d3Name = u"d3.geo.hammer"
        self.preview = "proj_hammer.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class healpix(projection):
    
    def __init__(self):
        self.name = u"HEALPix"
        self.d3Name = u"d3.geo.healpix"
        self.preview = "proj_healpix.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class hill(projection):

    def __init__(self):
        self.name = u"Hill Eucyclic"
        self.d3Name = u"d3.geo.hill"
        self.preview = "proj_hill.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class kavrayskiy7(projection):
    
    def __init__(self):
        self.name = u"Kavrayskiy VII"
        self.d3Name = u"d3.geo.kavrayskiy7"
        self.preview = "proj_kavrayskiy7.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class lagrange(projection):
    
    def __init__(self):
        self.name = u"Lagrange"
        self.d3Name = u"d3.geo.lagrange"
        self.preview = "proj_lagrange.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 
    
class conicConformal(projection):
    
    def __init__(self):
        self.name = u"Lambert Conic Conformal"
        self.d3Name = u"d3.geo.conicConformal"
        self.preview = "proj_lambert.png"
        
    def toScript(self, bound, width, height):
        return self.formatConicScript(bound, width, height) 

class larrivee(projection):

    def __init__(self):
        self.name = u"Larrivée"
        self.d3Name = u"d3.geo.larrivee"
        self.preview = "proj_larrivee.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 

class laskowski(projection):

    def __init__(self):
        self.name = u"Laskowski Tri-Optimal"
        self.d3Name = u"d3.geo.laskowski"
        self.preview = "proj_laskowski.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
        
class loximuthal(projection):
    
    def __init__(self):
        self.name = u"Loximuthal"
        self.d3Name = u"d3.geo.loximuthal"
        self.preview = "proj_loximuthal.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)         
        
class mercator(projection):
    
    def __init__(self):
        self.name = u"Mercator"
        self.d3Name = u"d3.geo.mercator"
        self.preview = "proj_mercator.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)  
    
class miller(projection):
    """Miller projection"""
    
    def __init__(self):
        self.name = u"Miller"
        self.d3Name = u"d3.geo.miller"
        self.preview = "proj_miller.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class mollweide(projection):
    
    def __init__(self):
        self.name = u"Mollweide"
        self.d3Name = u"d3.geo.mollweide"
        self.preview = "proj_mollweide.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class naturalEarth(projection):
    
    def __init__(self):
        self.name = u"Natural Earth"
        self.d3Name = u"d3.geo.naturalEarth"
        self.preview = "proj_naturalearth.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class nellHammer(projection):

    def __init__(self):
        self.name = u"Nell–Hammer"
        self.d3Name = u"d3.geo.nellHammer"
        self.preview = "proj_nellhammer.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class orthographic(projection):

    def __init__(self):
        self.name = u"Orthographic"
        self.d3Name = u"d3.geo.orthographic"
        self.preview = "proj_orthographic.png"
        
    def toScript(self, bound, width, height): 
        
        script = "{n}()\n      .center([{cx}, {cy}])\n      .scale(250)\n      .translate([width / 2, height / 2])\n      .clipAngle(90)"
        # TODO Scale needs calculating
        output = script.format(
            n = self.d3Name,
            cx = self.getCenterX(bound),
            cy = self.getCenterY(bound))

        return output 
    
    def zoomBehaviourScript(self):
        """Orthographic projections use d3.geo.zoom"""
        return """    svg.call(d3.geo.zoom().projection(projection).on("zoom", onZoom))"""
    
    def zoomScalingScript(self, outputLayers):
        """Orthographic version of the scaling script"""
        return """svg.selectAll("path").attr("d", path);"""
    
    def dragBehaviourScript(self):
        """Default drag behaviour script"""
        output = """\n    var drag = d3.behavior.drag().on("drag", function() {
      for (var i = 0; i < projections_.length; ++i) {
        var projection = projections_[i],
        angle = rotate(projection.rotate());
        projection.rotate(angle.rotate);
      }
      d3.select("#rotations").selectAll("svg").each(function(d) {
        d3.select(this).selectAll("path").attr("d", d.path);
      });
    });

    function rotate(rotate) { var angle = update(rotate); return {angle: angle, rotate: rotate}; }

    vectors.selectAll(".overlay").call(drag);\n"""

        return output


class patterson(projection):

    def __init__(self):
        self.name = u"Patterson Cylindrical"
        self.d3Name = u"d3.geo.patterson"
        self.preview = "proj_patterson.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class polyconic(projection):

    def __init__(self):
        self.name = u"Polyconic"
        self.d3Name = u"d3.geo.polyconic"
        self.preview = "proj_polyconic.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class robinson(projection):

    def __init__(self):
        self.name = u"Robinson"
        self.d3Name = u"d3.geo.robinson"
        self.preview = "proj_robinson.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height)
    
class sinusoidal(projection):
    
    def __init__(self):
        self.name = u"Sinusoidal"
        self.d3Name = u"d3.geo.sinusoidal"
        self.preview = "proj_sinusoidal.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class times(projection):
    
    def __init__(self):
        self.name = u"Times"
        self.d3Name = u"d3.geo.times"
        self.preview = "proj_times.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 

class vanDerGrinten(projection):
 
    def __init__(self):
        self.name = u"Van der Grinten I"
        self.d3Name = u"d3.geo.vanDerGrinten"
        self.preview = "proj_vandergrinten.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class vanDerGrinten2(projection):

    def __init__(self):
        self.name = u"Van der Grinten II"
        self.d3Name = u"d3.geo.vanDerGrinten2"
        self.preview = "proj_vandergrinten2.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class vanDerGrinten3(projection):

    def __init__(self):
        self.name = u"Van der Grinten III"
        self.d3Name = u"d3.geo.vanDerGrinten3"
        self.preview = "proj_vandergrinten3.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class vanDerGrinten4(projection):
    
    def __init__(self):
        self.name = u"Van der Grinten IV"
        self.d3Name = u"d3.geo.vanDerGrinten4"
        self.preview = "proj_vandergrinten4.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class wagner4(projection):

    def __init__(self):
        self.name = u"Wagner IV"
        self.d3Name = u"d3.geo.wagner4"
        self.preview = "proj_wagner4.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class wagner6(projection):
    
    def __init__(self):
        self.name = u"Wagner VI"
        self.d3Name = u"d3.geo.wagner6"
        self.preview = "proj_wagner6.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class wagner7(projection):    
    def __init__(self):
        self.name = u"Wagner VII"
        self.d3Name = u"d3.geo.wagner7"
        self.preview = "proj_wagner7.png"
        
    def toScript(self, bound, width, height): 
        return self.formatScript(bound, width, height) 
    
class winkelTripel(projection):

    def __init__(self):
        self.name = u"Winkel Tripel"
        self.d3Name = u"d3.geo.winkel3"
        self.preview = "proj_winkel3.png"
        
    def toScript(self, bound, width, height):
        return self.formatScript(bound, width, height) 