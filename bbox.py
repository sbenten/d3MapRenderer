import math

from logger import log

class bounds(list):
    """List of bounding boxes"""
    
    def __init__(self):
        """Constructor. Nothing special here"""
        self.__logger = log(self.__class__.__name__) 
        
               
    def getMaxBound(self):
        """Retrieve the maximum bounding box from each item in this list
        
        :returns: The maximum bounding box of all the boxes
        :rtype: bound
        """
        origLeft = 0.0
        maxLeft = 0.0
        origBottom = 0.0
        maxBottom = 0.0
        origRight = 0.0
        maxRight = 0.0
        origTop = 0.0
        maxTop = 0.0
        
        for b in self:
            if b.testLeft > maxLeft:
                maxLeft = b.testLeft
                origLeft = b.left
            if b.testBottom > maxBottom:
                maxBottom = b.testBottom  
                origBottom = b.bottom          
            if b.testRight > maxRight:
                maxRight = b.testRight  
                origRight = b.right
            if b.testTop > maxTop:
                maxTop = b.testTop  
                origTop = b.top
               
        self.__logger.info("Max bounds: " + str(origLeft) + " " + str(origBottom) + " " + str(origRight) + " " + str(origTop))       
        
        return bound(origLeft, origBottom, origRight, origTop)
    
class bound:
    """Bounding box of a layer"""
    
    def __init__(self, left, bottom, right, top):
        """Bounds constructor
        :param left: Minimum Longitude.
        :type left: float

        :param bottom: Minimum Latitudes.
        :type bottom: float
        
        :param right: Maximum Longitude.
        :type right: float
        
        :param top: Maximum Latitude.
        :type top: float
        """
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        # Make positive
        self.testLeft = math.sqrt(math.pow(self.left, 2))
        self.testBottom = math.sqrt(math.pow(self.bottom, 2))
        self.testRight = math.sqrt(math.pow(self.right, 2))
        self.testTop = math.sqrt(math.pow(self.top, 2))