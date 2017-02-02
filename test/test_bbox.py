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
import imp
b = imp.load_source('*', '../bbox.py')



class TestBBox(unittest.TestCase):
    """Test bounding boxes work."""
    
    def setUp(self):
        """Runs before each test."""
        self.afghanistan  = b.bound()
        self.afghanistan.setLeft(60.48574218750002)
        self.afghanistan.setBottom(29.391943359375)
        self.afghanistan.setRight(74.89130859375001)
        self.afghanistan.setTop(38.456396484375)
        self.argentina  = b.bound()
        self.argentina.setLeft(-73.57626953124998)
        self.argentina.setBottom(-55.032128906249945)
        self.argentina.setRight(-53.668554687500006)
        self.argentina.setTop(-21.802539062499974)
        self.bangladesh = b.bound()
        self.bangladesh.setLeft(88.02343750000003)
        self.bangladesh.setBottom(20.790429687500023)
        self.bangladesh.setRight(92.63164062500002)
        self.bangladesh.setTop(26.57153320312497)

        pass

    def tearDown(self):
        """Runs after each test."""
        pass
    
    def testBounds(self):
        """Check the params assigned correctly"""
        self.assertTrue(self.afghanistan.bottom == 29.391943359375, "What happened to the bottom property?")
        self.assertTrue(self.afghanistan.top == 38.456396484375, "What happened to the top property?")
        self.assertTrue(self.afghanistan.left == 60.48574218750002, "What happened to the left property?")
        self.assertTrue(self.afghanistan.right == 74.89130859375001, "What happened to the right property?")



if __name__ == '__main__':
    unittest.main()

