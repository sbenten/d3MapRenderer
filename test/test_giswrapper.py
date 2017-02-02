# coding=utf-8
"""Output test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
from nt import getcwd

__author__ = 'swbenten@gmail.com'
__date__ = '2015-10-09'
__copyright__ = 'Copyright 2015, Simon Benten'

import imp
import unittest
import os

from qgis.core import *
from qgis.gui import *

gisWrapper = imp.load_source('*', '../gisWrapper.py')

class TestGisWrapper(unittest.TestCase):
    """Test the output works
        Note: This doesn't check for pre-requisites"""

    def setUp(self):
        """Runs before each test."""  
        self.qgis = gisWrapper.qgisWrapper() 
        self.layer = None 
        self.srcpath = os.path.join(getcwd(), "src")
        self.destpath = os.path.join(getcwd(), "out")   
        self.shapefile = "ne__admin_countries_simp.shp"  
        self.objname = "something"     
        pass

    def tearDown(self):
        """Runs after each test."""
        
        del self.destLayer        
        pass
    
    def testOpen(self):        
        self.layer = self.qgis.openShape(os.path.join(self.srcpath, self.shapefile), self.objname)         
        self.assertTrue(self.layer is not None, "Failed to open the shapefile")
        self.assertTrue(self.layer.name == self.objname, "Layer name not set correctly")
        
    def testSave(self):
        self.qgis.saveShape(self.layer, os.path.join(self.destpath, self.shapeFile))
        self.assertTrue(os.path.isfile(os.path.join(self.destpath, self.shapeFile)), "Failed to save the shapefile. Shapefile doesn't exist where expected.")
    
if __name__ == '__main__':
    unittest.main()