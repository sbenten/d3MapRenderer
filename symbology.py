import sys
import traceback

from qgis.core import *
from PyQt4.QtCore import QVariant, Qt

from logger import log

class symbols(list):
    """Symbols list. Add only items from the sybmol class"""
    
    def __init__(self):
        """Constructor. Nothing special here"""
        
    def getAvergageOutlineWidth(self):
        """Retrieve the average outline width
        In theory each symbol could have a different outline width
        Zooming on the client requires scaling of the Svg border to maintain clarity
        However, re-scaling on each polygon/line/point is too costly
        Take the average width and do it to the entire group"""
        items = []
        for s in self:
            items.append(s.outlineWidth)
        average = sum(items) / float(len(items)) 
        return round(average, 4)
        
class singleSymbol:
    """Single symbol.Base class for tracking symbology within a layer"""
    
    def __init__(self, isMain, geoType, sym, css, trans):
        """Initialise the symbol range
  
        :param isMain: The main layer for the map
        :type isMain: boolean      
                
        :param geoType: Layer.geometryType() GeometryType of the layer.
        :type geoType: GeometryType  e.g. QGis.WKBPolygon
        
        :param sym: The symbol to use with this layer.
        :type sym: QgsSymbolV2
        
        :param css: Css class name to use.
        :type css: str
        
        :param trans: Transparency setting for the overall layer.
        :type trans: float
        
        """
        self.__logger = log(self.__class__.__name__) 
        self.isMain = isMain
        self.geometryType = geoType
        self.label = ""
        self.css = css
        self.transparency = trans
        self.outlineWidth = 0
        self.outlineColor = ""
        self.outlineStyle = None
        self.outlineTrans = 1.0
        self.color = sym.color().name()
        self.colorTrans = sym.color().alpha()
        self.symbolTrans = sym.alpha()
        self.brushStyle = 1
        
        self.outlineWidth, self.outlineColor, self.outlineStyle, self.outlineTrans, self.brushStyle = self.getOutlineDetails(sym)
        
        
    def getOutlineDetails(self, sym):
        
        outlineWidth = 0
        outlineColor = ""
        outlineStyle = None
        outlineTrans = 1.0
        brushStyle = 1
        
        t = type(sym)
        
        # different symbols have different attributes
        if t is QgsLineSymbolV2:
            outlineWidth = sym.width()
            outlineColor = sym.color().name()
            outlineTrans = sym.color().alpha()
        elif t is QgsMarkerSymbolV2:
            try:
                outlineColor = sym.symbolLayer(0).outlineColor().name()
                outlineWidth = sym.symbolLayer(0).outlineWidth()
                outlineStyle = sym.symbolLayer(0).outlineStyle()
            except AttributeError:
                outlineStyle = 1
            outlineTrans = sym.symbolLayer(0).outlineColor().alpha()
        elif t is QgsFillSymbolV2:
            try:
			    outlineWidth = sym.symbolLayer(0).borderWidth()
			    outlineColor = sym.symbolLayer(0).borderColor().name()
			    outlineTrans = sym.symbolLayer(0).borderColor().alpha() 
			    outlineStyle = sym.symbolLayer(0).borderStyle()
			    brushStyle =  sym.symbolLayer(0).brushStyle()
            except AttributeError:
                outlineWidth = 0.26        
        else: 
            # no idea what the symbol is, thrash around trying to guess the attributes            
            if sym.symbolLayer(0) is not None:
                try:
                    outlineWidth = sym.symbolLayer(0).borderWidth()
                    outlineColor = sym.symbolLayer(0).borderColor().name()
                    outlineStyle = sym.symbolLayer(0).borderStyle()
                    outlineTrans = sym.symbolLayer(0).borderColor().alpha()
                except AttributeError:
                    try:
                        outlineWidth = sym.symbolLayer(0).outlineWidth()
                        outlineColor = sym.symbolLayer(0).outlineColor().name()
                        outlineStyle = sym.symbolLayer(0).outlineStyle()
                        outlineTrans = sym.symbolLayer(0).outlineColor().alpha()
                    except AttributeError:
                        outlineWidth = sym.width()
                        outlineColor = sym.color().name()
                        outlineStyle = sym.penStyle()
                        outlineTrans = sym.color().alpha()
            else:
                outlineWidth = sym.width()
                outlineColor = sym.color().name()
                outlineStyle = sym.penStyle()
                outlineTrans = sym.color().alpha()
    
        return outlineWidth, outlineColor, outlineStyle, outlineTrans, brushStyle
        
    def getFilterExpression(self, isLowest):
        """Get the filter expression for selecting features based on their attribute"""
        # Single symbols apply to every feature
        return ""
        
    def isValueInRange(self, value):
        """Is the specified value in the range? Always is for single classification"""
        return True
    
    def getStyle(self):
        """Get the CSS style for the range"""
        if self.geometryType == 0:
            return self.getPointStyle()
        elif self.geometryType == 1:
            return self.getLineStyle()
        elif self.geometryType == 2 or self.geometryType == 3:
            return self.getPolygonStyle()
        else:
            return ""
        
    def getOpacity(self):
        """Get the opacity for the range"""
        opacity = "0"
        if self.brushStyle > 0: 
            '''
    Might implement this lot later, for now just interested in "No brush"
Qt::NoBrush    0    No brush pattern.
Qt::SolidPattern    1    Uniform color.
Qt::Dense1Pattern    2    Extremely dense brush pattern.
Qt::Dense2Pattern    3    Very dense brush pattern.
Qt::Dense3Pattern    4    Somewhat dense brush pattern.
Qt::Dense4Pattern    5    Half dense brush pattern.
Qt::Dense5Pattern    6    Somewhat sparse brush pattern.
Qt::Dense6Pattern    7    Very sparse brush pattern.
Qt::Dense7Pattern    8    Extremely sparse brush pattern.
Qt::HorPattern    9    Horizontal lines.
Qt::VerPattern    10    Vertical lines.
Qt::CrossPattern    11    Crossing horizontal and vertical lines.
Qt::BDiagPattern    12    Backward diagonal lines.
Qt::FDiagPattern    13    Forward diagonal lines.
Qt::DiagCrossPattern    14    Crossing diagonal lines.
Qt::LinearGradientPattern    15    Linear gradient (set using a dedicated QBrush constructor).
Qt::ConicalGradientPattern    17    Conical gradient (set using a dedicated QBrush constructor).
Qt::RadialGradientPattern    16    Radial gradient (set using a dedicated QBrush constructor).
Qt::TexturePattern    24    Custom pattern (see QBrush::setTexture())
            '''
            colorTrans = float(self.colorTrans)/255
            opacity = str(self.transparency  * self.symbolTrans * colorTrans)
        return opacity 
    
    
    def getOutlineOpacity(self):
        """Get the opacity for the range"""
        opacity = "0"
        if self.outlineStyle > 0:            
            colorTrans = float(self.outlineTrans)/255
            opacity = str(self.transparency  * self.symbolTrans * colorTrans)
        
        return opacity

    def getPointStyle(self):
        """Get the style for points. Only circles supported at the moment"""
        #TODO: Add other point shapes, by default d3 creates points as circles
        # Also sized circles will require some extra attribute setting 
        # as SVG circle radius is cannot be set by CSS. 
        # In D3 this needs setting "path.pointRadius(0.1);"
        val = ".{c} {b} {m}stroke: {s}; stroke-width: {w}; stroke-opacity: {so}; stroke-dasharray: {d}; fill: {f}; fill-opacity: {fo}; {e}"
        
        output = val.format(
            m = "pointer-events: none; " if self.isMain == False else "",
            c = self.css,
            b = "{",
            e = "}",
            s = unicode(self.outlineColor),
            w = unicode(self.outlineWidth),
            d = self.getBorderStyle(self.outlineStyle),
            f = unicode(self.color),
            fo = self.getOpacity(),
            so = self.getOutlineOpacity()) 
         
        return output
    
    def getLineStyle(self):
        """Get the style for graduated polygons"""
        val = ".{c} {b} {m}stroke: {s}; stroke-width: {w}; stroke-opacity: {o}; stroke-dasharray: {d}; fill-opacity: 0.0; {e}"
        output = val.format(
            m = "pointer-events: none; " if self.isMain == False else "",
            c = self.css,
            b = "{",
            e = "}",
            s = unicode(self.outlineColor),
            w = unicode(self.outlineWidth),
            d = self.getBorderStyle(self.outlineStyle),
            o = self.getOpacity())  
        
        return output
    
    
    def getPolygonStyle(self):
        """Get the style for graduated polygons"""
        val = ".{c} {b} {m}stroke: {s}; stroke-width: {w}; stroke-opacity: {so}; stroke-dasharray: {d}; fill: {f}; fill-opacity: {fo}; {e}"
        output = val.format(
            m = "pointer-events: none; " if self.isMain == False else "",
            c = self.css,
            b = "{",
            e = "}",
            s = unicode(self.outlineColor),
            w = unicode(self.outlineWidth),
            d = self.getBorderStyle(self.outlineStyle),
            f = unicode(self.color),
            fo = self.getOpacity(),
            so = self.getOutlineOpacity())      
        
        return output
    
    def getBorderStyle(self, style):
        """Get the line style applied to the border"""
        
        '''
Qt::NoPen    0    no line at all. For example, QPainter::drawRect() fills but does not draw any boundary line.
Qt::SolidLine    1    A plain line.
Qt::DashLine    2    Dashes separated by a few pixels.
Qt::DotLine    3    Dots separated by a few pixels.
Qt::DashDotLine    4    Alternate dots and dashes.
Qt::DashDotDotLine    5    One dash, two dots, one dash, two dots.
Qt::CustomDashLine    6    A custom pattern defined using QPainterPathStroker::setDashPattern()
        '''
        
        dash = ""
        if style > 1:
            if style == 2:
                dash = "10,5"
            if style == 3:
                dash = "1,5"
            if style == 4:
                dash = "15,5,1,5"
            if style == 5:
                dash = "15,5,1,5,1,5"
        
        return dash
   
class categorizedSymbol(singleSymbol):
    """Categorized sysmbol class"""
    
    def __init__(self, isMain, geoType, field, fieldType, range, css, trans):
        """Initialise the symbol range
  
        :param isMain: The main layer for the map
        :type isMain: boolean      
               
        :param geoType: Layer.geometryType() GeometryType of the layer.
        :type geoType: GeometryType  e.g. QGis.WKBPolygon
        
        :param field: Name of the attribute field used in the symbology
        :type field: str
        
        :param fieldType: Type of the attribute field used in the symbology (Integer, Real, String, Date)
        :type fieldType: str
        
        :param range: The range object.
        :type range: QgsRendererCategoryV2
        
        :param css: Css class name to use.
        :type css: str
        
        :param trans: Transparency setting for the overall layer.
        :type trans: float
        
        """
        self.__logger = log(self.__class__.__name__) 
        self.geometryType = geoType
        self.isMain = isMain
        self.field = field
        self.fieldType = fieldType
        self.label = range.label()
        self.value = str(range.value())
        self.css = css
        self.transparency = trans
        self.outlineWidth = 0
        self.outlineColor = ""
        self.outlineStyle = None
        self.outlineTrans = 1.0
        self.color = range.symbol().color().name()
        self.colorTrans = range.symbol().color().alpha()
        self.symbolTrans = range.symbol().alpha()
        self.brushStyle = 1
        
        self.outlineWidth, self.outlineColor, self.outlineStyle, self.outlineTrans, self.brushStyle = self.getOutlineDetails(range.symbol())
        
    def getFilterExpression(self, isLowest):
        """Get the filter expression for selecting features based on their attribute"""
        if self.fieldType == "String" or self.fieldType == "Date":
            output = "\"{c}\" = '{v}'"
            return output.format(
                c = self.field,
                v = self.value)
        else:
            output = "\"{c}\" = {v}"
            return output.format(
                c = self.field,
                v = self.value)
    
    def isValueInRange(self, value):
        """Is the specified value in the range?"""
        if self.value == value:
            return True
        else:
            return False
    
class graduatedSymbol(singleSymbol):
    """Graduated symbol class"""
    
    def __init__(self, isMain, geoType, field, range, css, trans):
        """Initialise the symbol range
  
        :param isMain: The main layer for the map
        :type isMain: boolean      
        
        :param geoType: Layer.geometryType() GeometryType of the layer.
        :type geoType: GeometryType  e.g. QGis.WKBPolygon
        
        :param field: Name of the attribute field used in the symbology
        :type field: str
        
        :param range: The range object.
        :type range: QgsRendererRangeV2
        
        :param css: Css class name to use.
        :type css: str
        
        :param trans: Transparency setting for the overall layer.
        :type trans: float
        
        """
        self.__logger = log(self.__class__.__name__) 
        self.isMain = isMain
        self.geometryType = geoType
        self.field = field
        self.label = str(range.label())
        self.value = str(range.lowerValue()) + " - " + str(range.upperValue())
        self.css = css
        self.transparency = trans
        # Range values are always numerics
        self.lowValue = range.lowerValue()
        self.highValue = range.upperValue()
        self.outlineWidth = 0.26
        self.outlineColor = ""
        self.outlineStyle = None
        self.outlineTrans = 1.0
        self.color = range.symbol().color().name()
        self.colorTrans = range.symbol().color().alpha()
        self.symbolTrans = range.symbol().alpha()
        self.brushStyle = 1
        
        self.outlineWidth, self.outlineColor, self.outlineStyle, self.outlineTrans, self.brushStyle = self.getOutlineDetails(range.symbol())
                    
    def getFilterExpression(self, isLowest):
        """Get the filter expression for selecting features based on their attribute"""
        lowRange = ">"
        if isLowest == True:
            lowRange = ">="
        output = "\"{c}\" {e} {l} and \"{c}\" <= {h}"
        return output.format(
            c = self.field,
            e = lowRange,
            l = self.lowValue,
            h = self.highValue)
    
    def isValueInRange(self, value):
        """Is the specified value in the range?"""
        if self.lowValue < value and self.highValue > value:
            return True
        else:
            return False