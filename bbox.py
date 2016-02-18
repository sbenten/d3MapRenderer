from __builtin__ import True
    
class bound:
    """Bounding box of a layer"""
    
    def __init__(self):
        """Bounds constructor
        
        bbox = left,bottom,right,top
        bbox = min Longitude , min Latitude , max Longitude , max Latitude
        Latitude is a decimal number between -90.0 and 90.0.
        Longitude is a decimal number between -180.0 and 180.0.
        
        src: http://wiki.openstreetmap.org/wiki/Bounding_Box"""
        
        self.left = -180.0
        self.bottom = -90.0
        self.right = 180.0
        self.top = 90.0
        
        self.inf = float("inf") 
        
    def setLeft(self, left):
        """Set the left extent of the bound
             
        :param left: Minimum Longitude.
        :type left: float"""
        
        if self.isInf(left) == False:
            self.left = left
        else:
            self.left = -180.0       


    def setBottom(self, bottom):
        """Set the bottom extent of the bound
             
        :param bottom: Minimum Latitudes.
        :type bottom: float"""
        
        if self.isInf(bottom) == False:
            self.bottom = bottom
        else:
            self.bottom = -90.0
            
                        
    def setRight(self, right):
        """Set the right extent of the bound
             
        :param right: Maximum Longitude.
        :type right: float"""
        
        if self.isInf(right) == False:
            self.right = right
        else:
            self.right = 180.0        
        
        
    def setTop(self, top):
        """Set the top extent of the bound
             
        :param top: Maximum Latitude.
        :type top: float   """
        
        if self.isInf(top) == False:
            self.top = top
        else:
            self.top = 90.0               
        
     
    def isInf(self, val):
        """Broken layers sometimes return "infinity" for the bounds"""
        if val == self.inf:
            return True
        else:
            return False
        