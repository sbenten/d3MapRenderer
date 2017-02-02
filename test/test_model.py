# coding=utf-8
"""Model test.

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

models = imp.load_source('*', '../models.py')
bbox = imp.load_source('*', '../bbox.py')
projections = imp.load_source('*', '../projections.py')



class TestModel(unittest.TestCase):
    """Test the output works
        Note: This doesn't check for pre-requisites"""

    def setUp(self):
        """Runs before each test."""            
        pass

    def tearDown(self):
        """Runs after each test."""
        pass
    
if __name__ == '__main__':
    unittest.main()