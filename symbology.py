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
    
    def __init__(self, geoType, sym, css, trans):
        """Initialise the symbol range
        
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
        
        self.outlineWidth, self.outlineColor, self.outlineStyle, self.outlineTrans = self.getOutlineDetails(sym)
        
        
    def getOutlineDetails(self, sym):
        
        outlineWidth = 0
        outlineColor = ""
        outlineStyle = None
        outlineTrans = 1.0
        
        t = type(sym)
        
        # different symbols have different attributes
        if t is QgsLineSymbolV2:
            outlineWidth = sym.width()
            outlineColor = sym.color().name()
            outlineTrans = sym.color().alpha()
        elif t is QgsMarkerSymbolV2:
            outlineWidth = sym.symbolLayer(0).outlineWidth()
            outlineColor = sym.symbolLayer(0).outlineColor().name()
            outlineStyle = sym.symbolLayer(0).outlineStyle()
            outlineTrans = sym.symbolLayer(0).outlineColor().alpha()
        elif t is QgsFillSymbolV2:
            outlineWidth = sym.symbolLayer(0).borderWidth()
            outlineColor = sym.symbolLayer(0).borderColor().name()
            outlineStyle = sym.symbolLayer(0).borderStyle()
            outlineTrans = sym.symbolLayer(0).borderColor().alpha()            
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
    
        return outlineWidth, outlineColor, outlineStyle, outlineTrans
        
    def getFilterExpression(self):
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
        colorTrans = float(self.colorTrans)/255
        return str(self.transparency  * self.symbolTrans * colorTrans)
    
    def getOutlineOpacity(self):
        """Get the opacity for the range"""
        colorTrans = float(self.outlineTrans)/255
        return str(self.transparency  * self.symbolTrans * colorTrans)

    def getPointStyle(self):
        """Get the style for points. Only circles supported at the moment"""
        #TODO: Add other point shapes, by default d3 creates points as circles
        # Also sized circles will require some extra attribute setting 
        # as SVG circle radius is cannot be set by CSS. 
        # In D3 this needs setting "path.pointRadius(0.1);"
        val = ".{c} {b} stroke: {s}; stroke-width: {w}; stroke-opacity: {so}; stroke-dasharray: {d}; fill: {f}; fill-opacity: {fo}; {e}"
        
        output = val.format(
            c = self.css,
            b = "{",
            e = "}",
            s = unicode(self.outlineColor),
            w = unicode(self.outlineWidth),
            d = self.getBorderStyle(self.outlineStyle),
            f = unicode(self.color),
            so = self.getOpacity(),
            fo = self.getOutlineOpacity()) 
         
        return output
    
    def getLineStyle(self):
        """Get the style for graduated polygons"""
        val = ".{c} {b} stroke: {s}; stroke-width: {w}; stroke-opacity: {o}; stroke-dasharray: {d}; fill-opacity: 0.0; {e}"
        output = val.format(
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
        val = ".{c} {b} stroke: {s}; stroke-width: {w}; stroke-opacity: {so}; stroke-dasharray: {d}; fill: {f}; fill-opacity: {fo}; {e}"
        output = val.format(
            c = self.css,
            b = "{",
            e = "}",
            s = unicode(self.outlineColor),
            w = unicode(self.outlineWidth),
            d = self.getBorderStyle(self.outlineStyle),
            f = unicode(self.color),
            so = self.getOpacity(),
            fo = self.getOutlineOpacity())      
        
        return output
    
    def getBorderStyle(self, style):
        """Get the line style applied to the border"""
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
    
    def __init__(self, geoType, field, fieldType, range, css, trans):
        """Initialise the symbol range
        
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
        
        self.outlineWidth, self.outlineColor, self.outlineStyle, self.outlineTrans = self.getOutlineDetails(range.symbol())
        
    def getFilterExpression(self):
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
    
    def __init__(self, geoType, field, range, css, trans):
        """Initialise the symbol range
        
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
        
        self.outlineWidth, self.outlineColor, self.outlineStyle, self.outlineTrans = self.getOutlineDetails(range.symbol())
                    
    def getFilterExpression(self):
        """Get the filter expression for selecting features based on their attribute"""
        output = "\"{c}\" >= {l} and \"{c}\" <= {h}"
        return output.format(
            c = self.field,
            l = self.lowValue,
            h = self.highValue)
    
    def isValueInRange(self, value):
        """Is the specified value in the range?"""
        if self.lowValue < value and self.highValue > value:
            return True
        else:
            return False