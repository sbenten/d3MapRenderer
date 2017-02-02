from logger import log

class css3(object):
    
    def __init__(self):
        """Constructor"""
        self.__logger = log(self.__class__.__name__)
    
    
    def getBorderStyle(self, style):
        """Get the line style applied to the border"""        
        """
Qt::NoPen    0    no line at all. For example, QPainter::drawRect() fills but does not draw any boundary line.
Qt::SolidLine    1    A plain line.
Qt::DashLine    2    Dashes separated by a few pixels.
Qt::DotLine    3    Dots separated by a few pixels.
Qt::DashDotLine    4    Alternate dots and dashes.
Qt::DashDotDotLine    5    One dash, two dots, one dash, two dots.
Qt::CustomDashLine    6    A custom pattern defined using QPainterPathStroker::setDashPattern()
        """
        
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
    
    def getOpacity(self, layerTrans, colorTrans, symbolTrans):
        """Get the opacity based on various transparency settings"""  
        return str(layerTrans  * symbolTrans * colorTrans)
    
    def convertColorTransToCssOpacity(self, colorTrans):
        """Convert a html color transpareny value (e.g. 0 - 255) to a css opacity value (e.g. 0.0 - 1.0)"""
        return float(colorTrans) / 255