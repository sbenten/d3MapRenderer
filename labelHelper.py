import sys
from qgis.core import *

class labeling:
    """Helper class for labeling"""  
    
    def __init__(self, layer):
        """Retrieve any label settings
        
        :param layer: The QgsVectorLayer to examine for label settings 
        :type layer: QgsVectorLayer   
        """
        self.enabled = (layer.customProperty("labeling/enabled", u"").lower() == "true")
        self.fieldName = layer.customProperty("labeling/fieldName", u"")
        self.fontFamily = layer.customProperty("labeling/fontFamily", u"")
        self.fontBold = (layer.customProperty("labeling/fontBold", u"").lower() == "true")
        self.fontItalic = (layer.customProperty("labeling/fontItalic", u"").lower() == "true")
        self.fontStrikeout = (layer.customProperty("labeling/fontStrikeout", u"").lower() == "true")
        self.fontUnderline = (layer.customProperty("labeling/fontUnderline", u"").lower() == "true")  
        self.fontSize = float(layer.customProperty("labeling/fontSize", "10")) 
  
        self.textColorA = int(layer.customProperty("labeling/textColorA", "255"))
        self.textColorB = int(layer.customProperty("labeling/textColorB", "0"))
        self.textColorG = int(layer.customProperty("labeling/textColorG", "0"))
        self.textColorR = int(layer.customProperty("labeling/textColorR", "0"))
        self.textTransparency = int(layer.customProperty("labeling/textTransp", "0")) 

        self.bufferDraw = (layer.customProperty("labeling/bufferDraw", u"").lower() == "true")
        self.bufferColorA = int(layer.customProperty("labeling/bufferColorA", "255"))
        self.bufferColorB = int(layer.customProperty("labeling/bufferColorB", "255"))
        self.bufferColorG = int(layer.customProperty("labeling/bufferColorG", "255"))
        self.bufferColorR = int(layer.customProperty("labeling/bufferColorR", "255"))
        self.bufferTransparency = int(layer.customProperty("labeling/bufferTransp", "0"))
        self.bufferSize = float(layer.customProperty("labeling/bufferSize", "1"))

        self.shadowDraw = (layer.customProperty("labeling/shadowDraw", u"").lower() == "true")
        self.shadowColorB = int(layer.customProperty("labeling/shadowColorB", "0"))
        self.shadowColorG = int(layer.customProperty("labeling/shadowColorG", "0"))
        self.shadowColorR = int(layer.customProperty("labeling/shadowColorR", "0"))
        self.shadowTransparency = int(layer.customProperty("labeling/shadowTransparency", "30"))
        self.shadowOffsetAngle = int(layer.customProperty("labeling/shadowOffsetAngle", "135"))
        self.shadowOffsetDist = int(layer.customProperty("labeling/shadowOffsetDist", "1"))
        self.shadowRadius = float(layer.customProperty("labeling/shadowRadius", "1.5"))
        
        self.placement = int(layer.customProperty("labeling/placement", "0"))
        self.quadOffset = int(layer.customProperty("labeling/quadOffset", "4"))
        
        self.isExpression = (layer.customProperty("labeling/isExpression", u"").lower() == "true")

    def hasLabels(self):
        """Does the layer have labels enabled and a field specified?
        At the moment expressions are not supported"""
        return self.enabled == True and self.fieldName != u"" and self.isExpression == False

    def toCss(self):
        """Convert the label settings to CSS3"""
        
        return """.label{b} 
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
        
        return output.join("")        
