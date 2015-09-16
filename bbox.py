import math

class bounds(list):
    """List of bounding boxes"""    
        
    def getMainBound(self):
        """Retrieve the bounding box for the main layer"""
        for b in self:
            if b.isMain == True:
               return b  
                     
        return None       
    
class bound:
    """Bounding box of a layer"""
    
    def __init__(self, isMain, left, bottom, right, top):
        """Bounds constructor
        :param isMain: Main layer
        :type isMain: boolean
        
        :param left: Minimum Longitude.
        :type left: string cast to float

        :param bottom: Minimum Latitudes.
        :type bottom: string cast to float
        
        :param right: Maximum Longitude.
        :type right: string cast to float
        
        :param top: Maximum Latitude.
        :type top: string cast to float        
        
        bbox = left,bottom,right,top
        bbox = min Longitude , min Latitude , max Longitude , max Latitude
        Latitude is a decimal number between -90.0 and 90.0.
        Longitude is a decimal number between -180.0 and 180.0.
        
        src: http://wiki.openstreetmap.org/wiki/Bounding_Box
        """
        
        self.isMain = isMain
        
        #broken layers sometimes return "infinity" for the bounds
        if left == "infinity":
            left = "-180.0"       
        if bottom == "infinity":
            bottom = "-90.0"    
        if right == "infinity":
            right = "180.0"       
        if top == "infinity":
            top = "90.0"   
            
        self.left = float(left)
        self.bottom = float(bottom)
        self.right = float(right)
        self.top = float(top)