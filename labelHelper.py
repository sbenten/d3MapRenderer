import sys
from qgis.core import *
from logger import log

class labeling(object):
    """Helper class for labeling"""  
    
    def __init__(self, layer, index):
        """Retrieve any label settings
        
        :param layer: The QgsVectorLayer to examine for label settings 
        :type layer: QgsVectorLayer   
        
        :param index: The index of the layer in the array of layers for output 
        :type index: int   
        
        """
        self.__logger = log(self.__class__.__name__)
        
        self.layer = layer
        self.index = index
        
        self.enabled = self.getBooleanProperty("labeling/enabled")
        self.fieldName = self.layer.customProperty("labeling/fieldName", u"")
        self.fontFamily = self.layer.customProperty("labeling/fontFamily", u"")
        self.fontBold = self.getBooleanProperty("labeling/fontBold")
        self.fontItalic = self.getBooleanProperty("labeling/fontItalic")
        self.fontStrikeout = self.getBooleanProperty("labeling/fontStrikeout")
        self.fontUnderline = self.getBooleanProperty("labeling/fontUnderline")  
        self.fontSize = float(self.layer.customProperty("labeling/fontSize", "10")) 
  
        self.textColorA = int(self.layer.customProperty("labeling/textColorA", "255"))
        self.textColorB = int(self.layer.customProperty("labeling/textColorB", "0"))
        self.textColorG = int(self.layer.customProperty("labeling/textColorG", "0"))
        self.textColorR = int(self.layer.customProperty("labeling/textColorR", "0"))
        self.textTransparency = int(self.layer.customProperty("labeling/textTransp", "0")) 

        self.bufferDraw = self.getBooleanProperty("labeling/bufferDraw")
        self.bufferColorA = int(self.layer.customProperty("labeling/bufferColorA", "255"))
        self.bufferColorB = int(self.layer.customProperty("labeling/bufferColorB", "255"))
        self.bufferColorG = int(self.layer.customProperty("labeling/bufferColorG", "255"))
        self.bufferColorR = int(self.layer.customProperty("labeling/bufferColorR", "255"))
        self.bufferTransparency = int(self.layer.customProperty("labeling/bufferTransp", "0"))
        self.bufferSize = float(self.layer.customProperty("labeling/bufferSize", "1"))

        self.shadowDraw = self.getBooleanProperty("labeling/shadowDraw")
        self.shadowColorB = int(self.layer.customProperty("labeling/shadowColorB", "0"))
        self.shadowColorG = int(self.layer.customProperty("labeling/shadowColorG", "0"))
        self.shadowColorR = int(self.layer.customProperty("labeling/shadowColorR", "0"))
        self.shadowTransparency = int(self.layer.customProperty("labeling/shadowTransparency", "30"))
        self.shadowOffsetAngle = int(self.layer.customProperty("labeling/shadowOffsetAngle", "135"))
        self.shadowOffsetDist = int(self.layer.customProperty("labeling/shadowOffsetDist", "1"))
        self.shadowRadius = float(self.layer.customProperty("labeling/shadowRadius", "1.5"))
        
        self.placement = int(self.layer.customProperty("labeling/placement", "0"))
        self.quadOffset = int(self.layer.customProperty("labeling/quadOffset", "4"))
        
        self.isExpression = self.getBooleanProperty("labeling/isExpression")

    def getBooleanProperty(self, prop):
        """Not all booleans are treated equally"""
        val = False
        
        try:
            # A real boolean?
            val = (self.layer.customProperty(prop, False) == True)
        except AttributeError:
            try:
                # A text value for a boolean?
                val = (self.layer.customProperty(prop, u"").lower() == "true")
            except AttributeError:
                self.__logger.info("No idea what the value for {0} is".format(prop))
                pass
            pass
    
        return val

    def hasLabels(self):
        """Does the layer have labels enabled and a field specified?
        At the moment expressions are not supported"""
        return self.enabled == True and self.fieldName != u"" and self.isExpression == False
    
    def getObjectScript(self):
        """Return the Javascript for creating the SVG text elements"""
        if self.hasLabels() == True:
            template = """      label{i} = vectors{i}.selectAll("text").data(object{i}.features);
      label{i}.enter()
        .append("text")
        .attr("x", function(d) {b} return path.centroid(d)[0]; {e})
        .attr("y", function(d) {b} return path.centroid(d)[1]; {e})
        .text(function(d) {b} return d.properties.{fieldName}; {e}})
        .attr("class", "label{i}");""".format(
                                              b = "{",
                                              i = self.index,
                                              fieldName = self.fieldName,
                                              e = "}")
            '''.attr("x", function (d) { return path.centroid(d)[0] > -1 ? 6 : -6;  })'''
            
        else:
            return ""
        
    def getZoomScript(self):
        """Return the script to resize SVG text elements"""
        if self.hasLabels() == True:
            return """label{i}.style("stroke-width", 0.2 / d3.event.scale);
      label{i}.style("font-size", labelSize(10, d3.event.scale)  + "pt");\n""".format(i = self.index)
        else:
            return ""   
    
    def getStyle(self):
        """Convert the label settings to CSS3"""
        if self.hasLabels() == True:
            return """.label{i}{b} 
    pointer-events: none; 
    {fill}
    {fontFamily}
    {fontSize} 
    {fontWeight}
    {fontStyle}
    {textDecoration}
    {fillOpacity} 
    {stroke}
    {strokeWidth} 
    {strokeOpacity}
    {textAnchor}
    {alignmentBaseline}
    {textShadow}
{e}""".format(              
           b = "{",
           i = self.index,
           fill = self.getFill(),
           fontFamily = self.getFontFamily(),
           fontSize = self.getFontSize(),
           fontWeight = self.getFontWeight(),
           fontStyle = self.getFontStyle(),
           textDecoration = self.getTextDecoraction(),
           fillOpacity = self.getFillOpacity(),
           stroke = self.getStroke(),
           strokeWidth = self.getStrokeWidth(),
           strokeOpacity = self.getStrokeOpacity(),
           textAnchor = self.getTextAnchor(),
           alignmentBaseline = self.getAlignmentBaseline(),
           textShadow = self.getTextShadow(),
           e = "}"
           )
        
        else:
            return ""


    def getFill(self): 
        template = "fill: rgba({r},{g},{b},{a});/n"
        
        return template.format(
                               r = str(self.textColorR),
                               g = str(self.textColorG),
                               b = str(self.textColorB),
                               a = str(self.textColorA)
                               )
        
    def getFillOpacity(self):
        template = "fill-opacity: {0};/n"
        
        return template.format(str(self.getOpacity(self.textTransparency)))
        
    def getOpacity(self, transparency):
        """Get the opacity value in a range between 1.0 (opaque) to 0 (transparent)
        Rather than as a percentage of transparency""" 
        return (100 - transparency) / 100  
        
    def getAlphaOpacity(self, alpha, transparency):
        """Get the opacity based on the color alpha and a transparency percentage"""
        colorTrans = float(transparency)/255
        
        return str(alpha * colorTrans)
    
    def getFontFamily(self):
        template = "font-family: {0};/n"
        
        if " " in self.fontFamily:
            self.fontFamily = "'{0}'".format(self.fontFamily)
    
        return template.format(self.fontFamily)
    
    def getFontSize(self):
        template = "font-size: {0}pt;/n"
        
        return template.format(str(self.fontSize))
    
    def getFontWeight(self):
        if self.fontBold == True:
            return "font-weight: bold;/n"
        else:
            return "font-weight: normal;/n"    

    def getFontStyle(self):
        if self.fontItalic == True:
            return "font-style: italic;/n"
        else:
            return "font-style: normal;/n"  
        
    def getTextDecoraction(self):
        if self.fontStrikeout == True or self.fontUnderline == True:
            template = "text-decoration:{0}{1};/n";
            underline = " underline" if self.fontUnderline == True  else ""
            strikeout = " line-through" if self.fontStrikeout == True  else ""
            
            return template.format(underline, strikeout)
        
        else:
            return "text-decoration:{0}{1};/n"
        
    def getStroke(self): 
        template = "stroke: rgba({r},{g},{b},{a});/n"
        
        return template.format(
                               r = str(self.textColorR),
                               g = str(self.textColorG),
                               b = str(self.textColorB),
                               a = str(self.textColorA)
                               )
        
    def getStrokeWidth(self):
        """At present QGIS does not allow the text outline to have a border
        Just set to 0.1 for now in order for advaned users to style it separately"""
        return "stroke-width = 0.1;/n"    
        
    def getStrokeOpacity(self):
        template = "stroke-opacity: {0};/n"
        
        return template.format(str(self.getOpacity(self.textTransparency)))        

    def getTextAnchor(self):
        """Text alignment Left -> Right
        QGIS labels have placement values of 0 = 'Around Centroid' aka centered, and 1 = 'Offset from Centroid'
        When using 'Offset from Centroid' the position can be top-left trough bottom-right with values such as:
        0 1 2
        3 4 5
        6 7 8"""
        template = "text-anchor: {0};/n"
        
        if self.placement == 1:            
            position = ["start", "middle", "end", "start", "middle", "end", "start", "middle", "end"]
            
            return template.format(position[self.quadOffset])
        else:
            return template.format("middle")
        
        
    def getAlignmentBaseline(self):
        """Text alignment Top -> Bottom
        QGIS labels have placement values of 0 = 'Around Centroid' aka centered, and 1 = 'Offset from Centroid'
        When using 'Offset from Centroid' the position can be top-left trough bottom-right with values such as:
        0 1 2
        3 4 5
        6 7 8"""
        template = "alignment-baseline: {0};/n"
        if self.placement == 1:
            position = ["alphabetic", "alphabetic", "alphabetic", "middle", "middle", "middle", "hanging", "hanging", "hanging"]
            
            return template.format(position[self.quadOffset])
        else:
            return template.format("middle") 
        
    def getTextShadow(self):
        """Get a text shadow to display any buffer and drop shadow implemented in the label
        NOTE: QGIS settings do not directly map onto CSS attributes""" 
        output = []
        
        if self.bufferDraw == True or self.shadowDraw == True:
            output.append("text-shadow: ")
            template = "{x}px {y}px {blur}px rgba({r},{g},{b},{a})"
                        
            if self.bufferDraw == True:
                output.append(template.format(
                                              x = "0",
                                              y = "0",
                                              blur = str(self.bufferSize * 3),
                                              r = self.bufferColorR,
                                              g = self.bufferColorG,
                                              b = self.bufferColorB,
                                              a = self.getAlphaOpacity(255, self.bufferTransparency)))
            
            if self.shadowDraw == True:
                if self.bufferDraw == True:
                    #text-shadow attributes are CSV
                    output.append(", ")    
                #CSS and QGIS differ on the starting angle. 
                #CSS is +90 degrees, starting at East on the compass
                angle = self.shadowOffsetAngle + 90 - 360 if self.shadowOffsetAngle + 90 > 359 else self.shadowOffsetAngle + 90
                posX = 2
                posY = 0
                if angle <= 10:
                    posX = 2
                    posY = 0
                elif angle >= 10 and angle < 45:
                    posX = 2
                    posY = 1
                elif angle >= 45 and angle < 55:
                    posX = 1
                    posY = 1
                elif angle >= 55 and angle < 90:
                    posX = 1
                    posY = 2
                elif angle >= 90 and angle < 125:
                    posX = 0
                    posY = 2
                elif angle >= 125 and angle < 135:
                    posX = -1
                    posY = 2
                elif angle >= 135 and angle < 140:
                    posX = -1
                    posY = 1
                elif angle >= 140 and angle < 170:
                    posX = -2
                    posY = 1
                elif angle >= 170 and angle < 185:
                    posX = -2
                    posY = 0
                elif angle >= 185 and angle < 225:
                    posX = -2
                    posY = -1
                elif angle >= 225 and angle < 235:
                    posX = -1
                    posY = -1
                elif angle >= 235 and angle < 260:
                    posX = -1
                    posY = -2
                elif angle >= 260 and angle < 285:
                    posX = 0
                    posY = -2                    
                elif angle >= 285 and angle < 315:
                    posX = 1
                    posY = -1
                elif angle >= 315 and angle < 350:
                    posX = 2
                    posY = -1
                else:
                    posX = 2
                    posY = 0
                    
                output.append(template.format(
                                              x = str(posX * self.shadowOffsetDist),
                                              y = str(posY * self.shadowOffsetDist),
                                              blur = str(self.shadowRadius * 3),
                                              r = self.shadowColorR,
                                              g = self.shadowColorG,
                                              b = self.shadowColorB,
                                              a = self.getAlphaOpacity(255, self.shadowTransparency)
                                              ))

                
          
                              
            output.append(";/n")
        
        return "".join(output)        
