# coding=utf-8
"""Output test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'swbenten@gmail.com'
__date__ = '2015-10-09'
__copyright__ = 'Copyright 2015, Simon Benten'

import imp
import unittest
import os

gisWrapper = imp.load_source('*', '../gisWrapper.py')

class TestGisWrapper(unittest.TestCase):
    """Test the output works
        Note: This doesn't check for pre-requisites"""

    def setUp(self):
        """Runs before each test."""  
        self.qgis = gisWrapper.qgisWrapper() 
        self.layer = None 
        self.srcpath = os.path.join(os.getcwd(), "src")
        self.destpath = os.path.join(os.getcwd(), "out")   
        self.shapefile = "ne__admin_countries_simp.shp"  
        self.objname = "something"     
        pass

    def tearDown(self):
        """Runs after each test."""
        
        del self.layer   
        filelist = [ f for f in os.listdir(self.destpath) if f.endswith(".forcecreation") == False ]
        for f in filelist:
            os.remove(os.path.join(self.destpath, f))     
        pass
    
    def testOpenSave(self):        
        self.layer = self.qgis.openShape(os.path.join(self.srcpath, self.shapefile), self.objname)         
        self.assertTrue(self.layer is not None, "Failed to open the shapefile")
        self.assertTrue(self.layer.name() == self.objname, "Layer name not set correctly")
        
        self.qgis.saveShape(self.layer, os.path.join(self.destpath, self.shapefile))
        self.assertTrue(os.path.isfile(os.path.join(self.destpath, self.shapefile)), "Failed to save the shapefile. Shapefile doesn't exist where expected.")
    
if __name__ == '__main__':
    unittest.main()