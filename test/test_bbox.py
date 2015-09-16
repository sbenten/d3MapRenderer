# coding=utf-8
"""Bounding box test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'swbenten@gmail.com'
__date__ = '2015-10-09'
__copyright__ = 'Copyright 2015, Simon Benten'

import unittest

import bbox 



class TestBBox(unittest.TestCase):
    """Test bouding boxes work."""
    
    def setUp(self):
        """Runs before each test."""
        self.afghanistan  = bbox.bound(True, 60.48574218750002, 29.391943359375, 74.89130859375001, 38.456396484375)
        self.argentina  = bbox.bound(True, -73.57626953124998, -55.032128906249945, -53.668554687500006, -21.802539062499974)
        self.bangladesh = bbox.bound(True, 88.02343750000003, 20.790429687500023, 92.63164062500002, 26.57153320312497)

        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def testMainExists(self):
        """Check the d3 names for projections are correct."""
        b = bbox.bounds()
        self.afghanistan.isMain = True
        b.append(self.afghanistan)
    
        self.assertIsNotNone(b.getMainBound(), "Where's Afghanistan gone?")
        
        #start again
        b[:] = []
        self.afghanistan.isMain = False
        b.append(self.afghanistan)
        self.argentina.isMain = True
        b.append(self.argentina)

        self.assertIsNotNone(b.getMainBound(), "Where's Argentina gone?")
        
        #start again
        b[:] = []
        self.afghanistan.isMain = False
        b.append(self.afghanistan)
        self.argentina.isMain = False
        b.append(self.argentina)
        self.bangladesh.isMain = True
        b.append(self.bangladesh)

        self.assertIsNotNone(b.getMainBound(), "Where's Bangladesh gone?")  
    
    def testMainNotExists(self):
        """Check the main bounds are not found"""
        b = bbox.bounds()
        self.afghanistan.isMain = False
        b.append(self.afghanistan)
    
        self.assertIsNone(b.getMainBound(), "Afghanistan should not be found!")
        
        #start again
        b[:] = []
        self.afghanistan.isMain = False
        b.append(self.afghanistan)
        self.argentina.isMain = False
        b.append(self.argentina)
        self.bangladesh.isMain = False
        b.append(self.bangladesh)

        self.assertIsNone(b.getMainBound(), "No country should be found!") 
    
    def testBounds(self):
        """Check the params assigned correctly"""
        self.assertTrue(self.afghanistan.bottom == 29.391943359375, "What happened to the bottom property?")
        self.assertTrue(self.afghanistan.top == 38.456396484375, "What happened to the top property?")
        self.assertTrue(self.afghanistan.left == 60.48574218750002, "What happened to the left property?")
        self.assertTrue(self.afghanistan.right == 74.89130859375001, "What happened to the right property?")



if __name__ == '__main__':
    unittest.main()

