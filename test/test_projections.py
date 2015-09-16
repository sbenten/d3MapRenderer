# coding=utf-8
"""Projections test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'swbenten@gmail.com'
__date__ = '2015-10-09'
__copyright__ = 'Copyright 2015, Simon Benten'

import unittest
import os
import bbox
import projections



class TestProjections(unittest.TestCase):
    """Test projections work."""

    def setUp(self):
        """Runs before each test."""
        self.projAitoff = projections.aitoff()
        self.projAlbers = projections.albers()
        self.projAlbersUsa = projections.albersUsa()
        self.projAugust = projections.august()
        self.projBaker = projections.baker()
        self.projBoggs = projections.boggs()
        self.projBromley = projections.bromley()
        self.projCollignon = projections.collignon()
        self.projConicConformal = projections.conicConformal()
        self.projConicEquidistant = projections.conicEquidistant()
        self.projCraster = projections.craster()
        self.projCylindricalEqualArea = projections.cylindricalEqualArea()
        self.projEckert1 = projections.eckert1()
        self.projEckert2 = projections.eckert2()
        self.projEckert3 = projections.eckert3()
        self.projEckert4 = projections.eckert4()
        self.projEckert5 = projections.eckert5()
        self.projEckert6 = projections.eckert6()
        self.projEisenlohr = projections.eisenlohr()
        self.projEquirectangular = projections.equirectangular()
        self.projFahey = projections.fahey()
        self.projMtFlatPolarParabolic = projections.mtFlatPolarParabolic()
        self.projMtFlatPolarQuartic = projections.mtFlatPolarQuartic()
        self.projMtFlatPolarSinusoidal = projections.mtFlatPolarSinusoidal()
        self.projGinzburg4 = projections.ginzburg4()
        self.projGinzburg5 = projections.ginzburg5()
        self.projGinzburg6 = projections.ginzburg6()
        self.projGinzburg8 = projections.ginzburg8()
        self.projGinzburg9 = projections.ginzburg9()
        self.projHomolosine = projections.homolosine()
        self.projGringorten = projections.gringorten()
        self.projGuyou = projections.guyou()
        self.projHammer = projections.hammer()
        self.projHEALPix = projections.healpix()
        self.projHill = projections.hill()
        self.projKavrayskiy7 = projections.kavrayskiy7()
        self.projLagrange = projections.lagrange()
        self.projLarrivee = projections.larrivee()
        self.projLaskowski = projections.laskowski()
        self.projLoximuthal = projections.loximuthal()
        self.projMercator = projections.mercator()
        self.projMollweide = projections.mollweide()
        self.projMiller = projections.miller()
        self.projNaturalEarth = projections.naturalEarth()
        self.projNellHammer = projections.nellHammer()
        self.projPatterson = projections.patterson()
        self.projPolyconic = projections.polyconic()
        self.projRobinson = projections.robinson()
        self.projSinusoidal = projections.sinusoidal()
        self.projTimes = projections.times()
        self.projVanDerGrinten = projections.vanDerGrinten()
        self.projVanDerGrinten2 = projections.vanDerGrinten2()
        self.projVanDerGrinten3 = projections.vanDerGrinten3()
        self.projVanDerGrinten4 = projections.vanDerGrinten4()
        self.projWagner4 = projections.wagner4()
        self.projWagner6 = projections.wagner6()
        self.projWagner7 = projections.wagner7()
        self.projWinkelTripel = projections.winkelTripel()   
        
        #Required for Albers projection tests
        #Values retrieved from exports of Natural Earth ne_50_admin_0_countries.shp filtered by "admin" field
        self.afghanistan  = bbox.bound(True, 60.48574218750002, 29.391943359375, 74.89130859375001, 38.456396484375)
        self.argentina  = bbox.bound(True, -73.57626953124998, -55.032128906249945, -53.668554687500006, -21.802539062499974)
        self.bangladesh = bbox.bound(True, 88.02343750000003, 20.790429687500023, 92.63164062500002, 26.57153320312497)
        self.belize = bbox.bound(True, -89.23749999999998, 15.888671875, -87.78862304687493, 18.482324218750023)
        self.bolivia  = bbox.bound(True, -69.645703125, -22.891699218750006, -57.49565429687499, -9.71044921875)
        self.burkinaFaso = bbox.bound(True, -5.523535156249977, 9.424707031249994, 2.38916015625, 15.077880859375)
        self.cambodia = bbox.bound(True, 102.31972656250005, 10.411230468749991, 107.60546874999997, 14.705078125)
        self.canada = bbox.bound(True, -141.00214843750004, 41.6748535156251, -52.653662109375034, 83.11611328125005)
        self.dominica = bbox.bound(True, -61.48115234375, 15.227294921875, -61.25107421874999, 15.633105468750003)
        self.ecuador = bbox.bound(True, -91.654150390625, -4.990625000000023, -75.24960937499998, 1.4553710937500313)
        self.egypt = bbox.bound(True, 24.703222656250006, 21.994873046875, 36.87138671875002, 31.654980468749997)
        self.estonia = bbox.bound(True, 21.854492187500057, 57.52548828124998, 28.15107421875004, 59.63901367187506)
        self.ethiopia = bbox.bound(True, 32.99892578125002, 3.4561035156249886, 47.97822265625001, 14.852294921875)
        self.fiji = bbox.bound(True, -180, -21.70585937499999, 180, -12.476953125000009)
        self.france = bbox.bound(True, -61.79409179687502, -21.369042968750037, 55.8390625000001, 51.097119140624955)
        self.germany = bbox.bound(True, 5.857519531250034, 47.27880859375003, 15.0166015625, 55.058740234374966)
        self.greenland = bbox.bound(True, -72.81806640624995, 59.815478515625045, -11.425537109374972, 83.59960937500006)
        self.greece = bbox.bound(True, 19.646484375, 34.93447265625002, 28.23183593750005, 41.74379882812502)
        self.iceland = bbox.bound(True, -24.475683593749977, 63.406689453125, -13.556103515624983, 66.52607421875)
        self.india = bbox.bound(True, 68.16503906250009, 6.748681640624994, 97.34355468750002, 35.49589843750002)
        self.iran = bbox.bound(True, 44.02324218750002, 25.102099609375017, 63.30517578124997, 39.76855468750006)
        self.japan = bbox.bound(True, 123.67978515625012, 24.266064453124955, 145.83300781249997, 45.509521484375)
        self.kenya = bbox.bound(True, 33.900000000000006, -4.692382812500014, 41.88398437500004, 5.492285156250006)
        self.madagascar = bbox.bound(True, 43.25712890625002, -25.57050781250004, 50.482714843750074, -12.079589843749957)
        self.malaysia = bbox.bound(True, 99.64628906250002, 0.8619628906250227, 119.2663085937501, 7.351660156250006)
        self.mexico = bbox.bound(True, -118.40136718749997, 14.545410156249986, -86.69628906249997, 32.71533203125003)
        self.morocco = bbox.bound(True, -17.003076171874937, 21.420703125000017, -1.0655273437499488, 35.929882812499955)
        self.namibia = bbox.bound(True, 11.7216796875, -28.938769531250003, 25.2587890625, -16.96767578125001)
        self.newZealand = bbox.bound(True, -176.84765625000003, -52.570312499999964, 178.53623046875006, -8.546484374999949)
        self.peru = bbox.bound(True, -81.33662109375, -18.34560546875001, -68.68525390625, -0.041748046875)
        self.poland = bbox.bound(True, 14.128613281250011, 49.020751953125, 24.105761718750017, 54.838183593749996)
        self.qatar = bbox.bound(True, 50.75458984375001, 24.564648437499997, 51.60888671875, 26.153271484374997)
        self.russia = bbox.bound(True, -180, 41.19926757812502, 180, 81.85419921874998)
        self.singapore = bbox.bound(True, 103.65019531249999, 1.265380859375, 103.99638671874999, 1.4470703124999886)
        self.somalia = bbox.bound(True, 40.964453125000006, -1.6953125, 51.390234375000006, 11.983691406249989)
        self.sweden = bbox.bound(True, 11.14716796875004, 55.34638671875004, 24.15546875000004, 69.036865234375)
        self.tonga = bbox.bound(True, -175.36235351562496, -21.450585937500037, -173.92187500000003, -18.565332031250023)
        self.USA = bbox.bound(True, -178.19453124999998, 18.963916015625074, 179.77998046875015, 71.40766601562501)
        self.yemen = bbox.bound(True, 42.5490234375001, 12.318994140624994, 54.511132812499994, 18.996142578125074)
        self.zimbabwe = bbox.bound(True, 25.224023437500023, -22.40205078125001, 33.00673828125002, -15.64306640625)
             
        pass

    def tearDown(self):
        """Runs after each test."""
        pass
    
    def testAlbersRotation(self):
        """Check that the albers projection (and therefore conic conformal as they are the same)
        returns the correct rotation"""

        rotation = self.projAlbers.getCenterX(self.greenland)
        self.assertEqual(rotation, 42, "Greenland rotation " + str(rotation) + " should be 42") 

        rotation = self.projAlbers.getCenterX(self.mexico)
        self.assertEqual(rotation, 102, "Mexico rotation " + str(rotation) + " should be 102")  
        
        rotation = self.projAlbers.getCenterX(self.morocco)
        self.assertEqual(rotation, 9, "Morocco rotation " + str(rotation) + " should be 9")   

        rotation = self.projAlbers.getCenterX(self.newZealand)
        self.assertEqual(rotation, 177, "New Zealand rotation " + str(rotation) + " should be 177")     
        
        rotation = self.projAlbers.getCenterX(self.peru)
        self.assertEqual(rotation, 75, "Peru rotation " + str(rotation) + " should be 75")  

        rotation = self.projAlbers.getCenterX(self.russia)
        self.assertEqual(rotation, 180, "Russia rotation " + str(rotation) + " should be 180")

        rotation = self.projAlbers.getCenterX(self.singapore)
        self.assertEqual(rotation, 103, "Singapore rotation " + str(rotation) + " should be 103")  

        rotation = self.projAlbers.getCenterX(self.somalia)
        self.assertEqual(rotation, 46, "Somalia rotation " + str(rotation) + " should be 46")  
        
        rotation = self.projAlbers.getCenterX(self.tonga)
        self.assertEqual(rotation, 174, "Tonga rotation " + str(rotation) + " should be 174") 

        """A bit strange, but given the addition of Hawaii and Alaska to the lower 48 
        this is actually rotated around the center, rather than the land mass and therefore correct"""
        rotation = self.projAlbers.getCenterX(self.USA)
        self.assertEqual(rotation, 178, "USA rotation " + str(rotation) + " should be 178") 
        
        rotation = self.projAlbers.getCenterX(self.yemen)
        self.assertEqual(rotation, 48, "Yemen rotation " + str(rotation) + " should be 48") 
        
        rotation = self.projAlbers.getCenterX(self.zimbabwe)
        self.assertEqual(rotation, 29, "Zimbabwe rotation " + str(rotation) + " should be 29") 
        

    def testD3Names(self):
        """Check the d3 names for projections are correct."""
        
        self.assertEqual(self.projAitoff.d3Name, u"d3.geo.aitoff")
        self.assertEqual(self.projAlbers.d3Name, u"d3.geo.albers")
        self.assertEqual(self.projAlbersUsa.d3Name, u"d3.geo.albersUsa")
        self.assertEqual(self.projAugust.d3Name, u"d3.geo.august")
        self.assertEqual(self.projBaker.d3Name, u"d3.geo.baker")
        self.assertEqual(self.projBoggs.d3Name, u"d3.geo.boggs")
        self.assertEqual(self.projBromley.d3Name, u"d3.geo.bromley")
        self.assertEqual(self.projCollignon.d3Name, u"d3.geo.collignon")
        self.assertEqual(self.projConicConformal.d3Name, u"d3.geo.conicConformal")
        self.assertEqual(self.projConicEquidistant.d3Name, u"d3.geo.conicEquidistant")
        self.assertEqual(self.projCraster.d3Name, u"d3.geo.craster")
        self.assertEqual(self.projCylindricalEqualArea.d3Name, u"d3.geo.cylindricalEqualArea")
        self.assertEqual(self.projEckert1.d3Name, u"d3.geo.eckert1")
        self.assertEqual(self.projEckert2.d3Name, u"d3.geo.eckert2")
        self.assertEqual(self.projEckert3.d3Name, u"d3.geo.eckert3")
        self.assertEqual(self.projEckert4.d3Name, u"d3.geo.eckert4")
        self.assertEqual(self.projEckert5.d3Name, u"d3.geo.eckert5")
        self.assertEqual(self.projEckert6.d3Name, u"d3.geo.eckert6")
        self.assertEqual(self.projEisenlohr.d3Name, u"d3.geo.eisenlohr")
        self.assertEqual(self.projEquirectangular.d3Name, u"d3.geo.equirectangular")
        self.assertEqual(self.projFahey.d3Name, u"d3.geo.fahey")
        self.assertEqual(self.projMtFlatPolarParabolic.d3Name, u"d3.geo.mtFlatPolarParabolic")
        self.assertEqual(self.projMtFlatPolarQuartic.d3Name, u"d3.geo.mtFlatPolarQuartic")
        self.assertEqual(self.projMtFlatPolarSinusoidal.d3Name, u"d3.geo.mtFlatPolarSinusoidal")
        self.assertEqual(self.projGinzburg4.d3Name, u"d3.geo.ginzburg4")
        self.assertEqual(self.projGinzburg5.d3Name, u"d3.geo.ginzburg5")
        self.assertEqual(self.projGinzburg6.d3Name, u"d3.geo.ginzburg6")
        self.assertEqual(self.projGinzburg8.d3Name, u"d3.geo.ginzburg8")
        self.assertEqual(self.projGinzburg9.d3Name, u"d3.geo.ginzburg9")
        self.assertEqual(self.projGringorten.d3Name, u"d3.geo.gringorten")
        self.assertEqual(self.projGuyou.d3Name, u"d3.geo.guyou")
        self.assertEqual(self.projHammer.d3Name, u"d3.geo.hammer")
        self.assertEqual(self.projHEALPix.d3Name, u"d3.geo.healpix")
        self.assertEqual(self.projHill.d3Name, u"d3.geo.hill")
        self.assertEqual(self.projHomolosine.d3Name, u"d3.geo.homolosine")
        self.assertEqual(self.projKavrayskiy7.d3Name, u"d3.geo.kavrayskiy7")
        self.assertEqual(self.projLagrange.d3Name, u"d3.geo.lagrange")
        self.assertEqual(self.projLarrivee.d3Name, u"d3.geo.larrivee")
        self.assertEqual(self.projLaskowski.d3Name, u"d3.geo.laskowski")
        self.assertEqual(self.projLoximuthal.d3Name, u"d3.geo.loximuthal")
        self.assertEqual(self.projMercator.d3Name, u"d3.geo.mercator")
        self.assertEqual(self.projMiller.d3Name, u"d3.geo.miller")
        self.assertEqual(self.projMollweide.d3Name, u"d3.geo.mollweide")
        self.assertEqual(self.projNaturalEarth.d3Name, u"d3.geo.naturalEarth")
        self.assertEqual(self.projNellHammer.d3Name, u"d3.geo.nellHammer")
        self.assertEqual(self.projPatterson.d3Name, u"d3.geo.patterson")
        self.assertEqual(self.projPolyconic.d3Name, u"d3.geo.polyconic")
        self.assertEqual(self.projRobinson.d3Name, u"d3.geo.robinson")
        self.assertEqual(self.projSinusoidal.d3Name, u"d3.geo.sinusoidal")
        self.assertEqual(self.projTimes.d3Name, u"d3.geo.times")
        self.assertEqual(self.projVanDerGrinten.d3Name, u"d3.geo.vanDerGrinten")
        self.assertEqual(self.projVanDerGrinten2.d3Name, u"d3.geo.vanDerGrinten2")
        self.assertEqual(self.projVanDerGrinten3.d3Name, u"d3.geo.vanDerGrinten3")
        self.assertEqual(self.projVanDerGrinten4.d3Name, u"d3.geo.vanDerGrinten4")
        self.assertEqual(self.projWagner4.d3Name, u"d3.geo.wagner4")
        self.assertEqual(self.projWagner6.d3Name, u"d3.geo.wagner6")
        self.assertEqual(self.projWagner7.d3Name, u"d3.geo.wagner7")
        self.assertEqual(self.projWinkelTripel.d3Name, u"d3.geo.winkel3")

    def testPreviewImages(self):
        """Check the d3 names for projections are correct."""        
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projAitoff.preview)), self.projAitoff.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projAlbers.preview)), self.projAlbers.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projAlbersUsa.preview)), self.projAlbersUsa.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projAugust.preview)), self.projAugust.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projBaker.preview)), self.projBaker.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projBoggs.preview)), self.projBoggs.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projBromley.preview)), self.projBromley.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projCollignon.preview)), self.projCollignon.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projConicConformal.preview)), self.projConicConformal.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projConicEquidistant.preview)), self.projConicEquidistant.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projCraster.preview)), self.projCraster.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projCylindricalEqualArea.preview)), self.projCylindricalEqualArea.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEckert1.preview)), self.projEckert1.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEckert2.preview)), self.projEckert2.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEckert3.preview)), self.projEckert3.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEckert4.preview)), self.projEckert4.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEckert5.preview)), self.projEckert5.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEckert6.preview)), self.projEckert6.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEisenlohr.preview)), self.projEisenlohr.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projEquirectangular.preview)), self.projEquirectangular.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projFahey.preview)), self.projFahey.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projMtFlatPolarParabolic.preview)), self.projMtFlatPolarParabolic.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projMtFlatPolarQuartic.preview)), self.projMtFlatPolarQuartic.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projMtFlatPolarSinusoidal.preview)), self.projMtFlatPolarSinusoidal.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGinzburg4.preview)), self.projGinzburg4.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGinzburg5.preview)), self.projGinzburg5.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGinzburg6.preview)), self.projGinzburg6.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGinzburg8.preview)), self.projGinzburg8.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGinzburg9.preview)), self.projGinzburg9.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGringorten.preview)), self.projGringorten.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projGuyou.preview)), self.projGuyou.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projHammer.preview)), self.projHammer.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projHEALPix.preview)), self.projHEALPix.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projHill.preview)), self.projHill.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projHomolosine.preview)), self.projHomolosine.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projKavrayskiy7.preview)), self.projKavrayskiy7.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projLagrange.preview)), self.projLagrange.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projLarrivee.preview)), self.projLarrivee.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projLaskowski.preview)), self.projLaskowski.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projLoximuthal.preview)), self.projLoximuthal.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projMercator.preview)), self.projMercator.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projMiller.preview)), self.projMiller.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projMollweide.preview)), self.projMollweide.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projNaturalEarth.preview)), self.projNaturalEarth.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projNellHammer.preview)), self.projNellHammer.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projPatterson.preview)), self.projPatterson.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projPolyconic.preview)), self.projPolyconic.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projRobinson.preview)), self.projRobinson.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projSinusoidal.preview)), self.projSinusoidal.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projTimes.preview)), self.projTimes.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projVanDerGrinten.preview)), self.projVanDerGrinten.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projVanDerGrinten2.preview)), self.projVanDerGrinten2.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projVanDerGrinten3.preview)), self.projVanDerGrinten3.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projVanDerGrinten4.preview)), self.projVanDerGrinten4.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projWagner4.preview)), self.projWagner4.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projWagner6.preview)), self.projWagner6.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projWagner7.preview)), self.projWagner7.preview)
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(projections.__file__), "img", self.projWinkelTripel.preview)), self.projWinkelTripel.preview)
        
        

if __name__ == '__main__':
    unittest.main()

'''
2015-09-10T14:17:42    0    model 2.10.1-Pisa
2015-09-10T14:17:42    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:17:42    0    topo Windows
2015-09-10T14:17:42    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:17:42    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:17:42    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:18:10    0    model EXPORT start ==================================================
2015-09-10T14:18:10    0    model        Title = [GD]
2015-09-10T14:18:10    0    model        Header = [False]
2015-09-10T14:18:10    0    model        Width = [800]
2015-09-10T14:18:10    0    model        Height = [600]
2015-09-10T14:18:10    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:18:10    0    model        IDField = [ID]
2015-09-10T14:18:10    0    model        Projection = [Aitoff]
2015-09-10T14:18:10    0    model        Simplify = []
2015-09-10T14:18:10    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:18:10    0    model        Zoom/Pan = [False]
2015-09-10T14:18:10    0    model        Legend = [False]
2015-09-10T14:18:10    0    model        LegendPos = [Top Left]
2015-09-10T14:18:10    0    model        IncExtras = [False]
2015-09-10T14:18:10    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:18:10    0    model        IncPopup = [False]
2015-09-10T14:18:10    0    model        PopupPos = [Bubble]
2015-09-10T14:18:10    0    model        Popup = []
2015-09-10T14:18:10    0    model        IncViz = [False]
2015-09-10T14:18:10    0    model        Chart = [Line Chart]
2015-09-10T14:18:10    0    model        VizWidth = [240]
2015-09-10T14:18:10    0    model        DataRanges = []
2015-09-10T14:18:10    0    model        Labels = []
2015-09-10T14:18:10    0    model EXPORT copying folders and files
2015-09-10T14:18:10    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:18:10    0    model Adding field: d3Css
2015-09-10T14:18:10    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:18:10    0    model setSingleSymbol
2015-09-10T14:18:10    0    model Filter: 
2015-09-10T14:18:10    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910141810\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910141810\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:18:11    0    winHelper topojson result 
            bounds: -178.19453124999998 18.963916015625074 179.77998046875015 71.40766601562501 (spherical)
            pre-quantization: 39.8m (0.000358Â°) 5.83m (0.0000524Â°)
            topology: 127 arcs, 5753 points
            post-quantization: 3.981km (0.0358Â°) 583m (0.00524Â°)
            prune: retained 127 / 127 arcs (100%)
            
2015-09-10T14:18:11    0    model d3.geo.aitoff()
                  .center([0, 45])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:18:11    0    model EXPORT complete =========================================================
2015-09-10T14:34:01    0    model 2.10.1-Pisa
2015-09-10T14:34:01    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:34:01    0    topo Windows
2015-09-10T14:34:01    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:34:01    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:34:01    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:34:13    0    model EXPORT start ==================================================
2015-09-10T14:34:13    0    model        Title = [zafgz]
2015-09-10T14:34:13    0    model        Header = [False]
2015-09-10T14:34:13    0    model        Width = [800]
2015-09-10T14:34:13    0    model        Height = [600]
2015-09-10T14:34:13    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:34:13    0    model        IDField = [ID]
2015-09-10T14:34:13    0    model        Projection = [Aitoff]
2015-09-10T14:34:13    0    model        Simplify = []
2015-09-10T14:34:13    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:34:13    0    model        Zoom/Pan = [False]
2015-09-10T14:34:13    0    model        Legend = [False]
2015-09-10T14:34:13    0    model        LegendPos = [Top Left]
2015-09-10T14:34:13    0    model        IncExtras = [False]
2015-09-10T14:34:13    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:34:13    0    model        IncPopup = [False]
2015-09-10T14:34:13    0    model        PopupPos = [Bubble]
2015-09-10T14:34:13    0    model        Popup = []
2015-09-10T14:34:13    0    model        IncViz = [False]
2015-09-10T14:34:13    0    model        Chart = [Line Chart]
2015-09-10T14:34:13    0    model        VizWidth = [240]
2015-09-10T14:34:13    0    model        DataRanges = []
2015-09-10T14:34:13    0    model        Labels = []
2015-09-10T14:34:13    0    model EXPORT copying folders and files
2015-09-10T14:34:13    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:34:13    0    model Adding field: d3Css
2015-09-10T14:34:13    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:34:13    0    model setSingleSymbol
2015-09-10T14:34:13    0    model Filter: 
2015-09-10T14:34:13    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143413\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143413\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:34:13    0    winHelper topojson result 
            bounds: 60.48574218750002 29.391943359375 74.89130859375001 38.456396484375 (spherical)
            pre-quantization: 1.60m (0.0000144Â°) 1.01m (0.00000907Â°)
            topology: 1 arcs, 410 points
            post-quantization: 160m (0.00144Â°) 101m (0.000907Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:34:13    0    model d3.geo.aitoff()
                  .center([67, 33])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:34:14    0    model EXPORT complete =========================================================
2015-09-10T14:35:20    0    model 2.10.1-Pisa
2015-09-10T14:35:20    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:35:20    0    topo Windows
2015-09-10T14:35:20    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:35:20    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:35:20    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:35:34    0    model EXPORT start ==================================================
2015-09-10T14:35:34    0    model        Title = [\\\\\]
2015-09-10T14:35:34    0    model        Header = [False]
2015-09-10T14:35:34    0    model        Width = [800]
2015-09-10T14:35:34    0    model        Height = [600]
2015-09-10T14:35:34    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:35:34    0    model        IDField = [ID]
2015-09-10T14:35:34    0    model        Projection = [Aitoff]
2015-09-10T14:35:34    0    model        Simplify = []
2015-09-10T14:35:34    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:35:34    0    model        Zoom/Pan = [False]
2015-09-10T14:35:34    0    model        Legend = [False]
2015-09-10T14:35:34    0    model        LegendPos = [Top Left]
2015-09-10T14:35:34    0    model        IncExtras = [False]
2015-09-10T14:35:34    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:35:34    0    model        IncPopup = [False]
2015-09-10T14:35:34    0    model        PopupPos = [Bubble]
2015-09-10T14:35:34    0    model        Popup = []
2015-09-10T14:35:34    0    model        IncViz = [False]
2015-09-10T14:35:34    0    model        Chart = [Line Chart]
2015-09-10T14:35:34    0    model        VizWidth = [240]
2015-09-10T14:35:34    0    model        DataRanges = []
2015-09-10T14:35:34    0    model        Labels = []
2015-09-10T14:35:34    0    model EXPORT copying folders and files
2015-09-10T14:35:34    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:35:34    0    model Adding field: d3Css
2015-09-10T14:35:34    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:35:34    0    model setSingleSymbol
2015-09-10T14:35:34    0    model Filter: 
2015-09-10T14:35:34    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143534\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143534\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:35:35    0    winHelper topojson result 
            bounds: -73.57626953124998 -55.032128906249945 -53.668554687500006 -21.802539062499974 (spherical)
            pre-quantization: 2.21m (0.0000199Â°) 3.70m (0.0000332Â°)
            topology: 4 arcs, 1039 points
            post-quantization: 221m (0.00199Â°) 370m (0.00332Â°)
            prune: retained 4 / 4 arcs (100%)
            
2015-09-10T14:35:35    0    model d3.geo.aitoff()
                  .center([-63, -38])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:35:35    0    model EXPORT complete =========================================================
2015-09-10T14:36:06    0    model 2.10.1-Pisa
2015-09-10T14:36:06    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:36:06    0    topo Windows
2015-09-10T14:36:06    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:36:06    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:36:06    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:36:18    0    model EXPORT start ==================================================
2015-09-10T14:36:18    0    model        Title = [\fb]
2015-09-10T14:36:18    0    model        Header = [False]
2015-09-10T14:36:18    0    model        Width = [800]
2015-09-10T14:36:18    0    model        Height = [600]
2015-09-10T14:36:18    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:36:18    0    model        IDField = [ID]
2015-09-10T14:36:18    0    model        Projection = [Aitoff]
2015-09-10T14:36:18    0    model        Simplify = []
2015-09-10T14:36:18    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:36:18    0    model        Zoom/Pan = [False]
2015-09-10T14:36:18    0    model        Legend = [False]
2015-09-10T14:36:18    0    model        LegendPos = [Top Left]
2015-09-10T14:36:18    0    model        IncExtras = [False]
2015-09-10T14:36:18    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:36:18    0    model        IncPopup = [False]
2015-09-10T14:36:18    0    model        PopupPos = [Bubble]
2015-09-10T14:36:18    0    model        Popup = []
2015-09-10T14:36:18    0    model        IncViz = [False]
2015-09-10T14:36:18    0    model        Chart = [Line Chart]
2015-09-10T14:36:18    0    model        VizWidth = [240]
2015-09-10T14:36:18    0    model        DataRanges = []
2015-09-10T14:36:18    0    model        Labels = []
2015-09-10T14:36:18    0    model EXPORT copying folders and files
2015-09-10T14:36:18    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:36:18    0    model Adding field: d3Css
2015-09-10T14:36:18    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:36:18    0    model setSingleSymbol
2015-09-10T14:36:18    0    model Filter: 
2015-09-10T14:36:18    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143618\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143618\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:36:19    0    winHelper topojson result 
            bounds: 88.02343750000003 20.790429687500023 92.63164062500002 26.57153320312497 (spherical)
            pre-quantization: 0.512m (0.00000461Â°) 0.643m (0.00000578Â°)
            topology: 7 arcs, 384 points
            post-quantization: 51.2m (0.000461Â°) 64.3m (0.000578Â°)
            prune: retained 7 / 7 arcs (100%)
            
2015-09-10T14:36:19    0    model d3.geo.aitoff()
                  .center([90, 23])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:36:19    0    model EXPORT complete =========================================================
2015-09-10T14:37:08    0    model 2.10.1-Pisa
2015-09-10T14:37:08    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:37:08    0    topo Windows
2015-09-10T14:37:08    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:37:08    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:37:08    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:37:19    0    model EXPORT start ==================================================
2015-09-10T14:37:19    0    model        Title = [afbga]
2015-09-10T14:37:19    0    model        Header = [False]
2015-09-10T14:37:19    0    model        Width = [800]
2015-09-10T14:37:19    0    model        Height = [600]
2015-09-10T14:37:19    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:37:19    0    model        IDField = [ID]
2015-09-10T14:37:19    0    model        Projection = [Aitoff]
2015-09-10T14:37:19    0    model        Simplify = []
2015-09-10T14:37:19    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:37:19    0    model        Zoom/Pan = [False]
2015-09-10T14:37:19    0    model        Legend = [False]
2015-09-10T14:37:19    0    model        LegendPos = [Top Left]
2015-09-10T14:37:19    0    model        IncExtras = [False]
2015-09-10T14:37:19    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:37:19    0    model        IncPopup = [False]
2015-09-10T14:37:19    0    model        PopupPos = [Bubble]
2015-09-10T14:37:19    0    model        Popup = []
2015-09-10T14:37:19    0    model        IncViz = [False]
2015-09-10T14:37:19    0    model        Chart = [Line Chart]
2015-09-10T14:37:19    0    model        VizWidth = [240]
2015-09-10T14:37:19    0    model        DataRanges = []
2015-09-10T14:37:19    0    model        Labels = []
2015-09-10T14:37:19    0    model EXPORT copying folders and files
2015-09-10T14:37:19    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:37:19    0    model Adding field: d3Css
2015-09-10T14:37:19    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:37:19    0    model setSingleSymbol
2015-09-10T14:37:19    0    model Filter: 
2015-09-10T14:37:19    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143719\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143719\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:37:20    0    winHelper topojson result 
            bounds: -89.23749999999998 15.888671875 -87.78862304687493 18.482324218750023 (spherical)
            pre-quantization: 0.161m (0.00000145Â°) 0.288m (0.00000259Â°)
            topology: 3 arcs, 65 points
            post-quantization: 16.1m (0.000145Â°) 28.8m (0.000259Â°)
            prune: retained 3 / 3 arcs (100%)
            
2015-09-10T14:37:20    0    model d3.geo.aitoff()
                  .center([-88, 17])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:37:20    0    model EXPORT complete =========================================================
2015-09-10T14:37:49    0    model 2.10.1-Pisa
2015-09-10T14:37:49    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:37:49    0    topo Windows
2015-09-10T14:37:49    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:37:49    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:37:49    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:37:57    0    model EXPORT start ==================================================
2015-09-10T14:37:57    0    model        Title = [\v]
2015-09-10T14:37:57    0    model        Header = [False]
2015-09-10T14:37:57    0    model        Width = [800]
2015-09-10T14:37:57    0    model        Height = [600]
2015-09-10T14:37:57    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:37:57    0    model        IDField = [ID]
2015-09-10T14:37:57    0    model        Projection = [Aitoff]
2015-09-10T14:37:57    0    model        Simplify = []
2015-09-10T14:37:57    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:37:57    0    model        Zoom/Pan = [False]
2015-09-10T14:37:57    0    model        Legend = [False]
2015-09-10T14:37:57    0    model        LegendPos = [Top Left]
2015-09-10T14:37:57    0    model        IncExtras = [False]
2015-09-10T14:37:57    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:37:57    0    model        IncPopup = [False]
2015-09-10T14:37:57    0    model        PopupPos = [Bubble]
2015-09-10T14:37:57    0    model        Popup = []
2015-09-10T14:37:57    0    model        IncViz = [False]
2015-09-10T14:37:57    0    model        Chart = [Line Chart]
2015-09-10T14:37:57    0    model        VizWidth = [240]
2015-09-10T14:37:57    0    model        DataRanges = []
2015-09-10T14:37:57    0    model        Labels = []
2015-09-10T14:37:57    0    model EXPORT copying folders and files
2015-09-10T14:37:57    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:37:57    0    model Adding field: d3Css
2015-09-10T14:37:57    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:37:57    0    model setSingleSymbol
2015-09-10T14:37:58    0    model Filter: 
2015-09-10T14:37:58    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143757\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143757\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:37:58    0    winHelper topojson result 
            bounds: -69.645703125 -22.891699218750006 -57.49565429687499 -9.71044921875 (spherical)
            pre-quantization: 1.35m (0.0000122Â°) 1.47m (0.0000132Â°)
            topology: 1 arcs, 418 points
            post-quantization: 135m (0.00122Â°) 147m (0.00132Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:37:58    0    model d3.geo.aitoff()
                  .center([-63, -16])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:37:58    0    model EXPORT complete =========================================================
2015-09-10T14:38:29    0    model 2.10.1-Pisa
2015-09-10T14:38:29    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:38:29    0    topo Windows
2015-09-10T14:38:29    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:38:29    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:38:29    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:38:43    0    model EXPORT start ==================================================
2015-09-10T14:38:43    0    model        Title = [\vc\]
2015-09-10T14:38:43    0    model        Header = [False]
2015-09-10T14:38:43    0    model        Width = [800]
2015-09-10T14:38:43    0    model        Height = [600]
2015-09-10T14:38:43    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:38:43    0    model        IDField = [ID]
2015-09-10T14:38:43    0    model        Projection = [Aitoff]
2015-09-10T14:38:43    0    model        Simplify = []
2015-09-10T14:38:43    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:38:43    0    model        Zoom/Pan = [False]
2015-09-10T14:38:43    0    model        Legend = [False]
2015-09-10T14:38:43    0    model        LegendPos = [Top Left]
2015-09-10T14:38:43    0    model        IncExtras = [False]
2015-09-10T14:38:43    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:38:43    0    model        IncPopup = [False]
2015-09-10T14:38:43    0    model        PopupPos = [Bubble]
2015-09-10T14:38:43    0    model        Popup = []
2015-09-10T14:38:43    0    model        IncViz = [False]
2015-09-10T14:38:43    0    model        Chart = [Line Chart]
2015-09-10T14:38:43    0    model        VizWidth = [240]
2015-09-10T14:38:43    0    model        DataRanges = []
2015-09-10T14:38:43    0    model        Labels = []
2015-09-10T14:38:43    0    model EXPORT copying folders and files
2015-09-10T14:38:43    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:38:43    0    model Adding field: d3Css
2015-09-10T14:38:43    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:38:43    0    model setSingleSymbol
2015-09-10T14:38:43    0    model Filter: 
2015-09-10T14:38:43    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143843\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143843\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:38:44    0    winHelper topojson result 
            bounds: -5.523535156249977 9.424707031249994 2.38916015625 15.077880859375 (spherical)
            pre-quantization: 0.880m (0.00000791Â°) 0.629m (0.00000565Â°)
            topology: 1 arcs, 253 points
            post-quantization: 88.0m (0.000791Â°) 62.9m (0.000565Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:38:44    0    model d3.geo.aitoff()
                  .center([-1, 12])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:38:44    0    model EXPORT complete =========================================================
2015-09-10T14:39:11    0    model 2.10.1-Pisa
2015-09-10T14:39:11    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:39:11    0    topo Windows
2015-09-10T14:39:11    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:39:11    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:39:11    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:39:21    0    model EXPORT start ==================================================
2015-09-10T14:39:21    0    model        Title = [b\b]
2015-09-10T14:39:21    0    model        Header = [False]
2015-09-10T14:39:21    0    model        Width = [800]
2015-09-10T14:39:21    0    model        Height = [600]
2015-09-10T14:39:21    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:39:21    0    model        IDField = [ID]
2015-09-10T14:39:21    0    model        Projection = [Aitoff]
2015-09-10T14:39:21    0    model        Simplify = []
2015-09-10T14:39:21    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:39:21    0    model        Zoom/Pan = [False]
2015-09-10T14:39:21    0    model        Legend = [False]
2015-09-10T14:39:21    0    model        LegendPos = [Top Left]
2015-09-10T14:39:21    0    model        IncExtras = [False]
2015-09-10T14:39:21    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:39:21    0    model        IncPopup = [False]
2015-09-10T14:39:21    0    model        PopupPos = [Bubble]
2015-09-10T14:39:21    0    model        Popup = []
2015-09-10T14:39:21    0    model        IncViz = [False]
2015-09-10T14:39:21    0    model        Chart = [Line Chart]
2015-09-10T14:39:21    0    model        VizWidth = [240]
2015-09-10T14:39:21    0    model        DataRanges = []
2015-09-10T14:39:21    0    model        Labels = []
2015-09-10T14:39:21    0    model EXPORT copying folders and files
2015-09-10T14:39:21    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:39:21    0    model Adding field: d3Css
2015-09-10T14:39:21    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:39:21    0    model setSingleSymbol
2015-09-10T14:39:21    0    model Filter: 
2015-09-10T14:39:21    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910143921\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910143921\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:39:21    0    winHelper topojson result 
            bounds: 102.31972656250005 10.411230468749991 107.60546874999997 14.705078125 (spherical)
            pre-quantization: 0.588m (0.00000529Â°) 0.478m (0.00000429Â°)
            topology: 3 arcs, 221 points
            post-quantization: 58.8m (0.000529Â°) 47.8m (0.000429Â°)
            prune: retained 3 / 3 arcs (100%)
            
2015-09-10T14:39:21    0    model d3.geo.aitoff()
                  .center([104, 12])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:39:21    0    model EXPORT complete =========================================================
2015-09-10T14:40:39    0    model 2.10.1-Pisa
2015-09-10T14:40:39    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:40:39    0    topo Windows
2015-09-10T14:40:39    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:40:39    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:40:39    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:40:49    0    model EXPORT start ==================================================
2015-09-10T14:40:49    0    model        Title = [zf]
2015-09-10T14:40:49    0    model        Header = [False]
2015-09-10T14:40:49    0    model        Width = [800]
2015-09-10T14:40:49    0    model        Height = [600]
2015-09-10T14:40:49    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:40:49    0    model        IDField = [ID]
2015-09-10T14:40:49    0    model        Projection = [Aitoff]
2015-09-10T14:40:49    0    model        Simplify = []
2015-09-10T14:40:49    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:40:49    0    model        Zoom/Pan = [False]
2015-09-10T14:40:49    0    model        Legend = [False]
2015-09-10T14:40:49    0    model        LegendPos = [Top Left]
2015-09-10T14:40:49    0    model        IncExtras = [False]
2015-09-10T14:40:49    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:40:49    0    model        IncPopup = [False]
2015-09-10T14:40:49    0    model        PopupPos = [Bubble]
2015-09-10T14:40:49    0    model        Popup = []
2015-09-10T14:40:49    0    model        IncViz = [False]
2015-09-10T14:40:49    0    model        Chart = [Line Chart]
2015-09-10T14:40:49    0    model        VizWidth = [240]
2015-09-10T14:40:49    0    model        DataRanges = []
2015-09-10T14:40:49    0    model        Labels = []
2015-09-10T14:40:49    0    model EXPORT copying folders and files
2015-09-10T14:40:49    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:40:49    0    model Adding field: d3Css
2015-09-10T14:40:49    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:40:49    0    model setSingleSymbol
2015-09-10T14:40:49    0    model Filter: 
2015-09-10T14:40:49    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144049\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144049\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:40:50    0    winHelper topojson result 
            bounds: -141.00214843750004 41.6748535156251 -52.653662109375034 83.11611328125005 (spherical)
            pre-quantization: 9.82m (0.0000884Â°) 4.61m (0.0000414Â°)
            topology: 141 arcs, 11573 points
            post-quantization: 982m (0.00884Â°) 461m (0.00414Â°)
            prune: retained 141 / 141 arcs (100%)
            
2015-09-10T14:40:50    0    model d3.geo.aitoff()
                  .center([-96, 62])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:40:50    0    model EXPORT complete =========================================================
2015-09-10T14:41:37    0    model 2.10.1-Pisa
2015-09-10T14:41:37    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:41:37    0    topo Windows
2015-09-10T14:41:37    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:41:37    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:41:37    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:41:51    0    model EXPORT start ==================================================
2015-09-10T14:41:51    0    model        Title = [zafbh]
2015-09-10T14:41:51    0    model        Header = [False]
2015-09-10T14:41:51    0    model        Width = [800]
2015-09-10T14:41:51    0    model        Height = [600]
2015-09-10T14:41:51    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:41:51    0    model        IDField = [ID]
2015-09-10T14:41:51    0    model        Projection = [Albers]
2015-09-10T14:41:51    0    model        Simplify = []
2015-09-10T14:41:51    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:41:51    0    model        Zoom/Pan = [False]
2015-09-10T14:41:51    0    model        Legend = [False]
2015-09-10T14:41:51    0    model        LegendPos = [Top Left]
2015-09-10T14:41:51    0    model        IncExtras = [False]
2015-09-10T14:41:51    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:41:51    0    model        IncPopup = [False]
2015-09-10T14:41:51    0    model        PopupPos = [Bubble]
2015-09-10T14:41:51    0    model        Popup = []
2015-09-10T14:41:51    0    model        IncViz = [False]
2015-09-10T14:41:51    0    model        Chart = [Line Chart]
2015-09-10T14:41:51    0    model        VizWidth = [240]
2015-09-10T14:41:51    0    model        DataRanges = []
2015-09-10T14:41:51    0    model        Labels = []
2015-09-10T14:41:51    0    model EXPORT copying folders and files
2015-09-10T14:41:51    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:41:51    0    model Adding field: d3Css
2015-09-10T14:41:51    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:41:51    0    model setSingleSymbol
2015-09-10T14:41:51    0    model Filter: 
2015-09-10T14:41:52    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144151\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144151\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:41:52    0    winHelper topojson result 
            bounds: -61.48115234375 15.227294921875 -61.25107421874999 15.633105468750003 (spherical)
            pre-quantization: 0.0256m (2.30e-7Â°) 0.0451m (4.06e-7Â°)
            topology: 1 arcs, 10 points
            post-quantization: 2.56m (0.0000230Â°) 4.51m (0.0000406Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:41:52    0    model d3.geo.albers()
                  .center([0, 15])
                  .rotate([61.0, 0])
                  .parallels([15, 16])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:41:52    0    model EXPORT complete =========================================================
2015-09-10T14:42:47    0    model 2.10.1-Pisa
2015-09-10T14:42:47    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:42:47    0    topo Windows
2015-09-10T14:42:47    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:42:47    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:42:47    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:43:06    0    model EXPORT start ==================================================
2015-09-10T14:43:06    0    model        Title = [ds]
2015-09-10T14:43:06    0    model        Header = [False]
2015-09-10T14:43:06    0    model        Width = [800]
2015-09-10T14:43:06    0    model        Height = [600]
2015-09-10T14:43:06    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:43:06    0    model        IDField = [ID]
2015-09-10T14:43:06    0    model        Projection = [Albers]
2015-09-10T14:43:06    0    model        Simplify = []
2015-09-10T14:43:06    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:43:06    0    model        Zoom/Pan = [False]
2015-09-10T14:43:06    0    model        Legend = [False]
2015-09-10T14:43:06    0    model        LegendPos = [Top Left]
2015-09-10T14:43:06    0    model        IncExtras = [False]
2015-09-10T14:43:06    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:43:06    0    model        IncPopup = [False]
2015-09-10T14:43:06    0    model        PopupPos = [Bubble]
2015-09-10T14:43:06    0    model        Popup = []
2015-09-10T14:43:06    0    model        IncViz = [False]
2015-09-10T14:43:06    0    model        Chart = [Line Chart]
2015-09-10T14:43:06    0    model        VizWidth = [240]
2015-09-10T14:43:06    0    model        DataRanges = []
2015-09-10T14:43:06    0    model        Labels = []
2015-09-10T14:43:06    0    model EXPORT copying folders and files
2015-09-10T14:43:06    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:43:07    0    model Adding field: d3Css
2015-09-10T14:43:07    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:43:07    0    model setSingleSymbol
2015-09-10T14:43:07    0    model Filter: 
2015-09-10T14:43:07    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144306\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144306\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:43:07    0    winHelper topojson result 
            bounds: -91.654150390625 -4.990625000000023 -75.24960937499998 1.4553710937500313 (spherical)
            pre-quantization: 1.82m (0.0000164Â°) 0.717m (0.00000645Â°)
            topology: 9 arcs, 347 points
            post-quantization: 182m (0.00164Â°) 71.7m (0.000645Â°)
            prune: retained 9 / 9 arcs (100%)
            
2015-09-10T14:43:07    0    model d3.geo.albers()
                  .center([0, -1])
                  .rotate([83.0, 0])
                  .parallels([-5, 2])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:43:07    0    model EXPORT complete =========================================================
2015-09-10T14:44:45    0    model 2.10.1-Pisa
2015-09-10T14:44:45    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:44:45    0    topo Windows
2015-09-10T14:44:45    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:44:45    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:44:45    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:44:59    0    model EXPORT start ==================================================
2015-09-10T14:44:59    0    model        Title = [zfb]
2015-09-10T14:44:59    0    model        Header = [False]
2015-09-10T14:44:59    0    model        Width = [800]
2015-09-10T14:44:59    0    model        Height = [600]
2015-09-10T14:44:59    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:44:59    0    model        IDField = [ID]
2015-09-10T14:44:59    0    model        Projection = [Albers]
2015-09-10T14:44:59    0    model        Simplify = []
2015-09-10T14:44:59    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:44:59    0    model        Zoom/Pan = [False]
2015-09-10T14:44:59    0    model        Legend = [False]
2015-09-10T14:44:59    0    model        LegendPos = [Top Left]
2015-09-10T14:44:59    0    model        IncExtras = [False]
2015-09-10T14:44:59    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:44:59    0    model        IncPopup = [False]
2015-09-10T14:44:59    0    model        PopupPos = [Bubble]
2015-09-10T14:44:59    0    model        Popup = []
2015-09-10T14:44:59    0    model        IncViz = [False]
2015-09-10T14:44:59    0    model        Chart = [Line Chart]
2015-09-10T14:44:59    0    model        VizWidth = [240]
2015-09-10T14:44:59    0    model        DataRanges = []
2015-09-10T14:44:59    0    model        Labels = []
2015-09-10T14:44:59    0    model EXPORT copying folders and files
2015-09-10T14:44:59    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:44:59    0    model Adding field: d3Css
2015-09-10T14:44:59    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:44:59    0    model setSingleSymbol
2015-09-10T14:44:59    0    model Filter: 
2015-09-10T14:45:00    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144459\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144459\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:45:00    0    winHelper topojson result 
            bounds: 24.703222656250006 21.994873046875 36.87138671875002 31.654980468749997 (spherical)
            pre-quantization: 1.35m (0.0000122Â°) 1.07m (0.00000966Â°)
            topology: 1 arcs, 253 points
            post-quantization: 135m (0.00122Â°) 107m (0.000966Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:45:00    0    model d3.geo.albers()
                  .center([0, 26])
                  .rotate([30.0, 0])
                  .parallels([21, 32])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:45:00    0    model EXPORT complete =========================================================
2015-09-10T14:45:49    0    model 2.10.1-Pisa
2015-09-10T14:45:49    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:45:49    0    topo Windows
2015-09-10T14:45:49    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:45:49    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:45:49    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:46:00    0    model EXPORT start ==================================================
2015-09-10T14:46:00    0    model        Title = [dga\]
2015-09-10T14:46:00    0    model        Header = [False]
2015-09-10T14:46:00    0    model        Width = [800]
2015-09-10T14:46:00    0    model        Height = [600]
2015-09-10T14:46:00    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:46:00    0    model        IDField = [ID]
2015-09-10T14:46:00    0    model        Projection = [Albers]
2015-09-10T14:46:00    0    model        Simplify = []
2015-09-10T14:46:00    0    model        Output = [D:\Downloads\Folder With Spaces]
2015-09-10T14:46:00    0    model        Zoom/Pan = [False]
2015-09-10T14:46:00    0    model        Legend = [False]
2015-09-10T14:46:00    0    model        LegendPos = [Top Left]
2015-09-10T14:46:00    0    model        IncExtras = [False]
2015-09-10T14:46:00    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:46:00    0    model        IncPopup = [False]
2015-09-10T14:46:00    0    model        PopupPos = [Bubble]
2015-09-10T14:46:00    0    model        Popup = []
2015-09-10T14:46:00    0    model        IncViz = [False]
2015-09-10T14:46:00    0    model        Chart = [Line Chart]
2015-09-10T14:46:00    0    model        VizWidth = [240]
2015-09-10T14:46:00    0    model        DataRanges = []
2015-09-10T14:46:00    0    model        Labels = []
2015-09-10T14:46:00    0    model EXPORT copying folders and files
2015-09-10T14:46:00    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:46:00    0    model Adding field: d3Css
2015-09-10T14:46:00    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:46:01    0    model setSingleSymbol
2015-09-10T14:46:01    0    model Filter: 
2015-09-10T14:46:01    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Folder With Spaces\20150910144600\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Folder With Spaces\20150910144600\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:46:01    0    winHelper topojson result 
            bounds: 21.854492187500057 57.52548828124998 28.15107421875004 59.63901367187506 (spherical)
            pre-quantization: 0.700m (0.00000630Â°) 0.235m (0.00000211Â°)
            topology: 4 arcs, 195 points
            post-quantization: 70.0m (0.000630Â°) 23.5m (0.000211Â°)
            prune: retained 4 / 4 arcs (100%)
            
2015-09-10T14:46:01    0    model d3.geo.albers()
                  .center([0, 58])
                  .rotate([25.0, 0])
                  .parallels([57, 60])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:46:01    0    model EXPORT complete =========================================================
2015-09-10T14:46:31    0    model 2.10.1-Pisa
2015-09-10T14:46:31    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:46:31    0    topo Windows
2015-09-10T14:46:31    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:46:31    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:46:31    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:46:42    0    model EXPORT start ==================================================
2015-09-10T14:46:42    0    model        Title = [\vg]
2015-09-10T14:46:42    0    model        Header = [False]
2015-09-10T14:46:42    0    model        Width = [800]
2015-09-10T14:46:42    0    model        Height = [600]
2015-09-10T14:46:42    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:46:42    0    model        IDField = [ID]
2015-09-10T14:46:42    0    model        Projection = [Albers]
2015-09-10T14:46:42    0    model        Simplify = []
2015-09-10T14:46:42    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:46:42    0    model        Zoom/Pan = [False]
2015-09-10T14:46:42    0    model        Legend = [False]
2015-09-10T14:46:42    0    model        LegendPos = [Top Left]
2015-09-10T14:46:42    0    model        IncExtras = [False]
2015-09-10T14:46:42    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:46:42    0    model        IncPopup = [False]
2015-09-10T14:46:42    0    model        PopupPos = [Bubble]
2015-09-10T14:46:42    0    model        Popup = []
2015-09-10T14:46:43    0    model        IncViz = [False]
2015-09-10T14:46:43    0    model        Chart = [Line Chart]
2015-09-10T14:46:43    0    model        VizWidth = [240]
2015-09-10T14:46:43    0    model        DataRanges = []
2015-09-10T14:46:43    0    model        Labels = []
2015-09-10T14:46:43    0    model EXPORT copying folders and files
2015-09-10T14:46:43    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:46:43    0    model Adding field: d3Css
2015-09-10T14:46:43    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:46:43    0    model setSingleSymbol
2015-09-10T14:46:43    0    model Filter: 
2015-09-10T14:46:43    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144643\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144643\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:46:43    0    winHelper topojson result 
            bounds: 32.99892578125002 3.4561035156249886 47.97822265625001 14.852294921875 (spherical)
            pre-quantization: 1.67m (0.0000150Â°) 1.27m (0.0000114Â°)
            topology: 1 arcs, 302 points
            post-quantization: 167m (0.00150Â°) 127m (0.00114Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:46:43    0    model d3.geo.albers()
                  .center([0, 9])
                  .rotate([40.0, 0])
                  .parallels([3, 15])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:46:43    0    model EXPORT complete =========================================================
2015-09-10T14:47:17    0    model 2.10.1-Pisa
2015-09-10T14:47:17    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:47:17    0    topo Windows
2015-09-10T14:47:17    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:47:17    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:47:17    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:47:29    0    model EXPORT start ==================================================
2015-09-10T14:47:29    0    model        Title = [adfg]
2015-09-10T14:47:29    0    model        Header = [False]
2015-09-10T14:47:29    0    model        Width = [800]
2015-09-10T14:47:29    0    model        Height = [600]
2015-09-10T14:47:29    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:47:29    0    model        IDField = [ID]
2015-09-10T14:47:29    0    model        Projection = [Albers]
2015-09-10T14:47:29    0    model        Simplify = []
2015-09-10T14:47:29    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:47:29    0    model        Zoom/Pan = [False]
2015-09-10T14:47:29    0    model        Legend = [False]
2015-09-10T14:47:29    0    model        LegendPos = [Top Left]
2015-09-10T14:47:29    0    model        IncExtras = [False]
2015-09-10T14:47:29    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:47:29    0    model        IncPopup = [False]
2015-09-10T14:47:29    0    model        PopupPos = [Bubble]
2015-09-10T14:47:29    0    model        Popup = []
2015-09-10T14:47:29    0    model        IncViz = [False]
2015-09-10T14:47:29    0    model        Chart = [Line Chart]
2015-09-10T14:47:29    0    model        VizWidth = [240]
2015-09-10T14:47:29    0    model        DataRanges = []
2015-09-10T14:47:29    0    model        Labels = []
2015-09-10T14:47:29    0    model EXPORT copying folders and files
2015-09-10T14:47:29    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:47:29    0    model Adding field: d3Css
2015-09-10T14:47:30    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:47:30    0    model setSingleSymbol
2015-09-10T14:47:30    0    model Filter: 
2015-09-10T14:47:30    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144729\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144729\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:47:30    0    winHelper topojson result 
            bounds: -180 -21.70585937499999 180 -12.476953125000009 (spherical)
            pre-quantization: 40.0m (0.000360Â°) 1.03m (0.00000923Â°)
            topology: 19 arcs, 272 points
            post-quantization: 4.003km (0.0360Â°) 103m (0.000923Â°)
            prune: retained 19 / 19 arcs (100%)
            
2015-09-10T14:47:30    0    model d3.geo.albers()
                  .center([0, -17])
                  .rotate([0.0, 0])
                  .parallels([-22, -12])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:47:30    0    model EXPORT complete =========================================================
2015-09-10T14:48:09    0    model 2.10.1-Pisa
2015-09-10T14:48:09    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:48:09    0    topo Windows
2015-09-10T14:48:09    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:48:10    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:48:10    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:48:29    0    model EXPORT start ==================================================
2015-09-10T14:48:29    0    model        Title = [France]
2015-09-10T14:48:29    0    model        Header = [False]
2015-09-10T14:48:29    0    model        Width = [800]
2015-09-10T14:48:29    0    model        Height = [600]
2015-09-10T14:48:29    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:48:29    0    model        IDField = [ID]
2015-09-10T14:48:29    0    model        Projection = [Albers]
2015-09-10T14:48:29    0    model        Simplify = []
2015-09-10T14:48:29    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:48:29    0    model        Zoom/Pan = [False]
2015-09-10T14:48:29    0    model        Legend = [False]
2015-09-10T14:48:29    0    model        LegendPos = [Top Left]
2015-09-10T14:48:29    0    model        IncExtras = [False]
2015-09-10T14:48:29    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:48:29    0    model        IncPopup = [False]
2015-09-10T14:48:29    0    model        PopupPos = [Bubble]
2015-09-10T14:48:29    0    model        Popup = []
2015-09-10T14:48:29    0    model        IncViz = [False]
2015-09-10T14:48:29    0    model        Chart = [Line Chart]
2015-09-10T14:48:29    0    model        VizWidth = [240]
2015-09-10T14:48:29    0    model        DataRanges = []
2015-09-10T14:48:29    0    model        Labels = []
2015-09-10T14:48:29    0    model EXPORT copying folders and files
2015-09-10T14:48:29    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:48:29    0    model Adding field: d3Css
2015-09-10T14:48:29    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:48:29    0    model setSingleSymbol
2015-09-10T14:48:29    0    model Filter: 
2015-09-10T14:48:29    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144829\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144829\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:48:29    0    winHelper topojson result 
            bounds: -61.79409179687502 -21.369042968750037 55.8390625000001 51.097119140624955 (spherical)
            pre-quantization: 13.1m (0.000118Â°) 8.06m (0.0000725Â°)
            topology: 10 arcs, 817 points
            post-quantization: 1.308km (0.0118Â°) 806m (0.00725Â°)
            prune: retained 10 / 10 arcs (100%)
            
2015-09-10T14:48:29    0    model d3.geo.albers()
                  .center([0, 14])
                  .rotate([2.0, 0])
                  .parallels([-22, 52])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:48:29    0    model EXPORT complete =========================================================
2015-09-10T14:49:01    0    model 2.10.1-Pisa
2015-09-10T14:49:01    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:49:01    0    topo Windows
2015-09-10T14:49:01    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:49:01    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:49:01    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:49:16    0    model EXPORT start ==================================================
2015-09-10T14:49:16    0    model        Title = [Germany]
2015-09-10T14:49:16    0    model        Header = [False]
2015-09-10T14:49:16    0    model        Width = [800]
2015-09-10T14:49:16    0    model        Height = [600]
2015-09-10T14:49:16    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:49:16    0    model        IDField = [ID]
2015-09-10T14:49:16    0    model        Projection = [Albers]
2015-09-10T14:49:16    0    model        Simplify = []
2015-09-10T14:49:16    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:49:16    0    model        Zoom/Pan = [False]
2015-09-10T14:49:16    0    model        Legend = [False]
2015-09-10T14:49:16    0    model        LegendPos = [Top Left]
2015-09-10T14:49:16    0    model        IncExtras = [False]
2015-09-10T14:49:16    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:49:16    0    model        IncPopup = [False]
2015-09-10T14:49:16    0    model        PopupPos = [Bubble]
2015-09-10T14:49:16    0    model        Popup = []
2015-09-10T14:49:16    0    model        IncViz = [False]
2015-09-10T14:49:16    0    model        Chart = [Line Chart]
2015-09-10T14:49:16    0    model        VizWidth = [240]
2015-09-10T14:49:16    0    model        DataRanges = []
2015-09-10T14:49:16    0    model        Labels = []
2015-09-10T14:49:16    0    model EXPORT copying folders and files
2015-09-10T14:49:16    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:49:16    0    model Adding field: d3Css
2015-09-10T14:49:16    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:49:16    0    model setSingleSymbol
2015-09-10T14:49:16    0    model Filter: 
2015-09-10T14:49:16    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910144916\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910144916\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:49:17    0    winHelper topojson result 
            bounds: 5.857519531250034 47.27880859375003 15.0166015625 55.058740234374966 (spherical)
            pre-quantization: 1.02m (0.00000916Â°) 0.865m (0.00000778Â°)
            topology: 6 arcs, 562 points
            post-quantization: 102m (0.000916Â°) 86.5m (0.000778Â°)
            prune: retained 6 / 6 arcs (100%)
            
2015-09-10T14:49:17    0    model d3.geo.albers()
                  .center([0, 51])
                  .rotate([10.0, 0])
                  .parallels([47, 56])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:49:17    0    model EXPORT complete =========================================================
2015-09-10T14:49:59    0    model 2.10.1-Pisa
2015-09-10T14:49:59    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:49:59    0    topo Windows
2015-09-10T14:49:59    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:49:59    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:49:59    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:50:15    0    model EXPORT start ==================================================
2015-09-10T14:50:15    0    model        Title = [Greenland]
2015-09-10T14:50:15    0    model        Header = [False]
2015-09-10T14:50:15    0    model        Width = [800]
2015-09-10T14:50:15    0    model        Height = [600]
2015-09-10T14:50:15    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:50:15    0    model        IDField = [ID]
2015-09-10T14:50:15    0    model        Projection = [Albers]
2015-09-10T14:50:15    0    model        Simplify = []
2015-09-10T14:50:15    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:50:15    0    model        Zoom/Pan = [False]
2015-09-10T14:50:15    0    model        Legend = [False]
2015-09-10T14:50:15    0    model        LegendPos = [Top Left]
2015-09-10T14:50:15    0    model        IncExtras = [False]
2015-09-10T14:50:15    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:50:15    0    model        IncPopup = [False]
2015-09-10T14:50:15    0    model        PopupPos = [Bubble]
2015-09-10T14:50:15    0    model        Popup = []
2015-09-10T14:50:15    0    model        IncViz = [False]
2015-09-10T14:50:15    0    model        Chart = [Line Chart]
2015-09-10T14:50:15    0    model        VizWidth = [240]
2015-09-10T14:50:15    0    model        DataRanges = []
2015-09-10T14:50:15    0    model        Labels = []
2015-09-10T14:50:15    0    model EXPORT copying folders and files
2015-09-10T14:50:15    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:50:15    0    model Adding field: d3Css
2015-09-10T14:50:15    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:50:15    0    model setSingleSymbol
2015-09-10T14:50:15    0    model Filter: 
2015-09-10T14:50:16    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145015\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145015\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:50:16    0    winHelper topojson result 
            bounds: -72.81806640624995 59.815478515625045 -11.425537109374972 83.59960937500006 (spherical)
            pre-quantization: 6.83m (0.0000614Â°) 2.64m (0.0000238Â°)
            topology: 17 arcs, 2240 points
            post-quantization: 683m (0.00614Â°) 264m (0.00238Â°)
            prune: retained 17 / 17 arcs (100%)
            
2015-09-10T14:50:16    0    model d3.geo.albers()
                  .center([0, 71])
                  .rotate([42.0, 0])
                  .parallels([59, 84])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:50:16    0    model EXPORT complete =========================================================
2015-09-10T14:50:45    0    model 2.10.1-Pisa
2015-09-10T14:50:45    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:50:45    0    topo Windows
2015-09-10T14:50:45    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:50:45    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:50:45    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:51:00    0    model EXPORT start ==================================================
2015-09-10T14:51:00    0    model        Title = [Greece]
2015-09-10T14:51:00    0    model        Header = [False]
2015-09-10T14:51:00    0    model        Width = [800]
2015-09-10T14:51:00    0    model        Height = [600]
2015-09-10T14:51:00    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:51:00    0    model        IDField = [ID]
2015-09-10T14:51:00    0    model        Projection = [Albers]
2015-09-10T14:51:00    0    model        Simplify = []
2015-09-10T14:51:00    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:51:00    0    model        Zoom/Pan = [False]
2015-09-10T14:51:00    0    model        Legend = [False]
2015-09-10T14:51:00    0    model        LegendPos = [Top Left]
2015-09-10T14:51:00    0    model        IncExtras = [False]
2015-09-10T14:51:00    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:51:00    0    model        IncPopup = [False]
2015-09-10T14:51:00    0    model        PopupPos = [Bubble]
2015-09-10T14:51:00    0    model        Popup = []
2015-09-10T14:51:00    0    model        IncViz = [False]
2015-09-10T14:51:00    0    model        Chart = [Line Chart]
2015-09-10T14:51:00    0    model        VizWidth = [240]
2015-09-10T14:51:00    0    model        DataRanges = []
2015-09-10T14:51:00    0    model        Labels = []
2015-09-10T14:51:00    0    model EXPORT copying folders and files
2015-09-10T14:51:00    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:51:00    0    model Adding field: d3Css
2015-09-10T14:51:00    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:51:00    0    model setSingleSymbol
2015-09-10T14:51:00    0    model Filter: 
2015-09-10T14:51:00    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145100\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145100\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:51:01    0    winHelper topojson result 
            bounds: 19.646484375 34.93447265625002 28.23183593750005 41.74379882812502 (spherical)
            pre-quantization: 0.955m (0.00000859Â°) 0.757m (0.00000681Â°)
            topology: 40 arcs, 923 points
            post-quantization: 95.5m (0.000859Â°) 75.7m (0.000681Â°)
            prune: retained 40 / 40 arcs (100%)
            
2015-09-10T14:51:01    0    model d3.geo.albers()
                  .center([0, 38])
                  .rotate([23.0, 0])
                  .parallels([34, 42])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:51:01    0    model EXPORT complete =========================================================
2015-09-10T14:51:41    0    model 2.10.1-Pisa
2015-09-10T14:51:41    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:51:41    0    topo Windows
2015-09-10T14:51:41    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:51:41    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:51:41    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:51:58    0    model EXPORT start ==================================================
2015-09-10T14:51:58    0    model        Title = [Iceland]
2015-09-10T14:51:58    0    model        Header = [False]
2015-09-10T14:51:58    0    model        Width = [800]
2015-09-10T14:51:58    0    model        Height = [600]
2015-09-10T14:51:58    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:51:58    0    model        IDField = [ID]
2015-09-10T14:51:58    0    model        Projection = [Albers]
2015-09-10T14:51:58    0    model        Simplify = []
2015-09-10T14:51:58    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:51:58    0    model        Zoom/Pan = [False]
2015-09-10T14:51:58    0    model        Legend = [False]
2015-09-10T14:51:58    0    model        LegendPos = [Top Left]
2015-09-10T14:51:58    0    model        IncExtras = [False]
2015-09-10T14:51:58    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:51:58    0    model        IncPopup = [False]
2015-09-10T14:51:58    0    model        PopupPos = [Bubble]
2015-09-10T14:51:58    0    model        Popup = []
2015-09-10T14:51:58    0    model        IncViz = [False]
2015-09-10T14:51:58    0    model        Chart = [Line Chart]
2015-09-10T14:51:58    0    model        VizWidth = [240]
2015-09-10T14:51:58    0    model        DataRanges = []
2015-09-10T14:51:58    0    model        Labels = []
2015-09-10T14:51:58    0    model EXPORT copying folders and files
2015-09-10T14:51:58    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:51:58    0    model Adding field: d3Css
2015-09-10T14:51:58    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:51:58    0    model setSingleSymbol
2015-09-10T14:51:58    0    model Filter: 
2015-09-10T14:51:58    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145158\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145158\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:51:58    0    winHelper topojson result 
            bounds: -24.475683593749977 63.406689453125 -13.556103515624983 66.52607421875 (spherical)
            pre-quantization: 1.21m (0.0000109Â°) 0.347m (0.00000312Â°)
            topology: 1 arcs, 453 points
            post-quantization: 121m (0.00109Â°) 34.7m (0.000312Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:51:58    0    model d3.geo.albers()
                  .center([0, 64])
                  .rotate([19.0, 0])
                  .parallels([63, 67])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:51:58    0    model EXPORT complete =========================================================
2015-09-10T14:52:21    0    model 2.10.1-Pisa
2015-09-10T14:52:21    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:52:21    0    topo Windows
2015-09-10T14:52:21    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:52:21    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:52:21    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:52:36    0    model EXPORT start ==================================================
2015-09-10T14:52:36    0    model        Title = [India]
2015-09-10T14:52:36    0    model        Header = [False]
2015-09-10T14:52:36    0    model        Width = [800]
2015-09-10T14:52:36    0    model        Height = [600]
2015-09-10T14:52:36    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:52:36    0    model        IDField = [ID]
2015-09-10T14:52:36    0    model        Projection = [Albers]
2015-09-10T14:52:36    0    model        Simplify = []
2015-09-10T14:52:36    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:52:36    0    model        Zoom/Pan = [False]
2015-09-10T14:52:36    0    model        Legend = [False]
2015-09-10T14:52:36    0    model        LegendPos = [Top Left]
2015-09-10T14:52:36    0    model        IncExtras = [False]
2015-09-10T14:52:36    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:52:36    0    model        IncPopup = [False]
2015-09-10T14:52:36    0    model        PopupPos = [Bubble]
2015-09-10T14:52:36    0    model        Popup = []
2015-09-10T14:52:36    0    model        IncViz = [False]
2015-09-10T14:52:36    0    model        Chart = [Line Chart]
2015-09-10T14:52:36    0    model        VizWidth = [240]
2015-09-10T14:52:36    0    model        DataRanges = []
2015-09-10T14:52:36    0    model        Labels = []
2015-09-10T14:52:36    0    model EXPORT copying folders and files
2015-09-10T14:52:36    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:52:36    0    model Adding field: d3Css
2015-09-10T14:52:36    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:52:36    0    model setSingleSymbol
2015-09-10T14:52:37    0    model Filter: 
2015-09-10T14:52:37    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145236\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145236\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:52:37    0    winHelper topojson result 
            bounds: 68.16503906250009 6.748681640624994 97.34355468750002 35.49589843750002 (spherical)
            pre-quantization: 3.24m (0.0000292Â°) 3.20m (0.0000288Â°)
            topology: 14 arcs, 1521 points
            post-quantization: 324m (0.00292Â°) 320m (0.00288Â°)
            prune: retained 14 / 14 arcs (100%)
            
2015-09-10T14:52:37    0    model d3.geo.albers()
                  .center([0, 21])
                  .rotate([82.0, 0])
                  .parallels([6, 36])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:52:37    0    model EXPORT complete =========================================================
2015-09-10T14:53:13    0    model 2.10.1-Pisa
2015-09-10T14:53:13    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:53:13    0    topo Windows
2015-09-10T14:53:13    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:53:13    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:53:13    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:53:29    0    model EXPORT start ==================================================
2015-09-10T14:53:29    0    model        Title = [Iran]
2015-09-10T14:53:29    0    model        Header = [False]
2015-09-10T14:53:29    0    model        Width = [800]
2015-09-10T14:53:29    0    model        Height = [600]
2015-09-10T14:53:29    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:53:29    0    model        IDField = [ID]
2015-09-10T14:53:29    0    model        Projection = [Albers]
2015-09-10T14:53:29    0    model        Simplify = []
2015-09-10T14:53:29    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:53:29    0    model        Zoom/Pan = [False]
2015-09-10T14:53:29    0    model        Legend = [False]
2015-09-10T14:53:29    0    model        LegendPos = [Top Left]
2015-09-10T14:53:29    0    model        IncExtras = [False]
2015-09-10T14:53:29    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:53:29    0    model        IncPopup = [False]
2015-09-10T14:53:29    0    model        PopupPos = [Bubble]
2015-09-10T14:53:29    0    model        Popup = []
2015-09-10T14:53:29    0    model        IncViz = [False]
2015-09-10T14:53:29    0    model        Chart = [Line Chart]
2015-09-10T14:53:29    0    model        VizWidth = [240]
2015-09-10T14:53:29    0    model        DataRanges = []
2015-09-10T14:53:29    0    model        Labels = []
2015-09-10T14:53:29    0    model EXPORT copying folders and files
2015-09-10T14:53:29    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:53:29    0    model Adding field: d3Css
2015-09-10T14:53:29    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:53:29    0    model setSingleSymbol
2015-09-10T14:53:29    0    model Filter: 
2015-09-10T14:53:29    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145329\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145329\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:53:29    0    winHelper topojson result 
            bounds: 44.02324218750002 25.102099609375017 63.30517578124997 39.76855468750006 (spherical)
            pre-quantization: 2.14m (0.0000193Â°) 1.63m (0.0000147Â°)
            topology: 2 arcs, 606 points
            post-quantization: 214m (0.00193Â°) 163m (0.00147Â°)
            prune: retained 2 / 2 arcs (100%)
            
2015-09-10T14:53:29    0    model d3.geo.albers()
                  .center([0, 32])
                  .rotate([53.0, 0])
                  .parallels([25, 40])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:53:29    0    model EXPORT complete =========================================================
2015-09-10T14:54:00    0    model 2.10.1-Pisa
2015-09-10T14:54:00    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:54:00    0    topo Windows
2015-09-10T14:54:00    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:54:00    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:54:00    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:54:15    0    model EXPORT start ==================================================
2015-09-10T14:54:15    0    model        Title = [Japan]
2015-09-10T14:54:15    0    model        Header = [False]
2015-09-10T14:54:15    0    model        Width = [800]
2015-09-10T14:54:15    0    model        Height = [600]
2015-09-10T14:54:15    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:54:15    0    model        IDField = [ID]
2015-09-10T14:54:15    0    model        Projection = [Albers]
2015-09-10T14:54:15    0    model        Simplify = []
2015-09-10T14:54:15    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:54:15    0    model        Zoom/Pan = [False]
2015-09-10T14:54:15    0    model        Legend = [False]
2015-09-10T14:54:15    0    model        LegendPos = [Top Left]
2015-09-10T14:54:15    0    model        IncExtras = [False]
2015-09-10T14:54:15    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:54:15    0    model        IncPopup = [False]
2015-09-10T14:54:15    0    model        PopupPos = [Bubble]
2015-09-10T14:54:15    0    model        Popup = []
2015-09-10T14:54:15    0    model        IncViz = [False]
2015-09-10T14:54:15    0    model        Chart = [Line Chart]
2015-09-10T14:54:15    0    model        VizWidth = [240]
2015-09-10T14:54:15    0    model        DataRanges = []
2015-09-10T14:54:15    0    model        Labels = []
2015-09-10T14:54:15    0    model EXPORT copying folders and files
2015-09-10T14:54:15    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:54:15    0    model Adding field: d3Css
2015-09-10T14:54:15    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:54:15    0    model setSingleSymbol
2015-09-10T14:54:15    0    model Filter: 
2015-09-10T14:54:15    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145415\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145415\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:54:15    0    winHelper topojson result 
            bounds: 123.67978515625012 24.266064453124955 145.83300781249997 45.509521484375 (spherical)
            pre-quantization: 2.46m (0.0000222Â°) 2.36m (0.0000212Â°)
            topology: 34 arcs, 1097 points
            post-quantization: 246m (0.00222Â°) 236m (0.00212Â°)
            prune: retained 34 / 34 arcs (100%)
            
2015-09-10T14:54:15    0    model d3.geo.albers()
                  .center([0, 34])
                  .rotate([134.0, 0])
                  .parallels([24, 46])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:54:15    0    model EXPORT complete =========================================================
2015-09-10T14:54:41    0    model 2.10.1-Pisa
2015-09-10T14:54:41    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:54:41    0    topo Windows
2015-09-10T14:54:41    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:54:41    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:54:41    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:54:57    0    model EXPORT start ==================================================
2015-09-10T14:54:57    0    model        Title = [Kenya]
2015-09-10T14:54:57    0    model        Header = [False]
2015-09-10T14:54:57    0    model        Width = [800]
2015-09-10T14:54:57    0    model        Height = [600]
2015-09-10T14:54:57    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:54:57    0    model        IDField = [ID]
2015-09-10T14:54:57    0    model        Projection = [Albers]
2015-09-10T14:54:57    0    model        Simplify = []
2015-09-10T14:54:57    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:54:57    0    model        Zoom/Pan = [False]
2015-09-10T14:54:57    0    model        Legend = [False]
2015-09-10T14:54:57    0    model        LegendPos = [Top Left]
2015-09-10T14:54:57    0    model        IncExtras = [False]
2015-09-10T14:54:57    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:54:57    0    model        IncPopup = [False]
2015-09-10T14:54:57    0    model        PopupPos = [Bubble]
2015-09-10T14:54:57    0    model        Popup = []
2015-09-10T14:54:57    0    model        IncViz = [False]
2015-09-10T14:54:57    0    model        Chart = [Line Chart]
2015-09-10T14:54:57    0    model        VizWidth = [240]
2015-09-10T14:54:57    0    model        DataRanges = []
2015-09-10T14:54:57    0    model        Labels = []
2015-09-10T14:54:57    0    model EXPORT copying folders and files
2015-09-10T14:54:57    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:54:57    0    model Adding field: d3Css
2015-09-10T14:54:57    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:54:57    0    model setSingleSymbol
2015-09-10T14:54:57    0    model Filter: 
2015-09-10T14:54:57    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145457\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145457\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:54:58    0    winHelper topojson result 
            bounds: 33.900000000000006 -4.692382812500014 41.88398437500004 5.492285156250006 (spherical)
            pre-quantization: 0.888m (0.00000798Â°) 1.13m (0.0000102Â°)
            topology: 2 arcs, 225 points
            post-quantization: 88.8m (0.000798Â°) 113m (0.00102Â°)
            prune: retained 2 / 2 arcs (100%)
            
2015-09-10T14:54:58    0    model d3.geo.albers()
                  .center([0, 0])
                  .rotate([37.0, 0])
                  .parallels([-5, 6])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:54:58    0    model EXPORT complete =========================================================
2015-09-10T14:56:02    0    model 2.10.1-Pisa
2015-09-10T14:56:02    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:56:02    0    topo Windows
2015-09-10T14:56:02    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:56:02    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:56:02    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:56:18    0    model EXPORT start ==================================================
2015-09-10T14:56:18    0    model        Title = [Madagascar]
2015-09-10T14:56:18    0    model        Header = [False]
2015-09-10T14:56:18    0    model        Width = [800]
2015-09-10T14:56:18    0    model        Height = [600]
2015-09-10T14:56:18    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:56:18    0    model        IDField = [ID]
2015-09-10T14:56:18    0    model        Projection = [Albers]
2015-09-10T14:56:18    0    model        Simplify = []
2015-09-10T14:56:18    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:56:18    0    model        Zoom/Pan = [False]
2015-09-10T14:56:18    0    model        Legend = [False]
2015-09-10T14:56:18    0    model        LegendPos = [Top Left]
2015-09-10T14:56:18    0    model        IncExtras = [False]
2015-09-10T14:56:18    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:56:18    0    model        IncPopup = [False]
2015-09-10T14:56:18    0    model        PopupPos = [Bubble]
2015-09-10T14:56:18    0    model        Popup = []
2015-09-10T14:56:18    0    model        IncViz = [False]
2015-09-10T14:56:18    0    model        Chart = [Line Chart]
2015-09-10T14:56:18    0    model        VizWidth = [240]
2015-09-10T14:56:18    0    model        DataRanges = []
2015-09-10T14:56:18    0    model        Labels = []
2015-09-10T14:56:18    0    model EXPORT copying folders and files
2015-09-10T14:56:18    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:56:18    0    model Adding field: d3Css
2015-09-10T14:56:18    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:56:18    0    model setSingleSymbol
2015-09-10T14:56:18    0    model Filter: 
2015-09-10T14:56:19    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145618\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145618\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:56:19    0    winHelper topojson result 
            bounds: 43.25712890625002 -25.57050781250004 50.482714843750074 -12.079589843749957 (spherical)
            pre-quantization: 0.804m (0.00000723Â°) 1.50m (0.0000135Â°)
            topology: 3 arcs, 266 points
            post-quantization: 80.4m (0.000723Â°) 150m (0.00135Â°)
            prune: retained 3 / 3 arcs (100%)
            
2015-09-10T14:56:19    0    model d3.geo.albers()
                  .center([0, -18])
                  .rotate([46.0, 0])
                  .parallels([-26, -12])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:56:19    0    model EXPORT complete =========================================================
2015-09-10T14:56:46    0    model 2.10.1-Pisa
2015-09-10T14:56:46    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:56:46    0    topo Windows
2015-09-10T14:56:46    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:56:46    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:56:46    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:57:01    0    model EXPORT start ==================================================
2015-09-10T14:57:01    0    model        Title = [Malaysia]
2015-09-10T14:57:01    0    model        Header = [False]
2015-09-10T14:57:01    0    model        Width = [800]
2015-09-10T14:57:01    0    model        Height = [600]
2015-09-10T14:57:01    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:57:01    0    model        IDField = [ID]
2015-09-10T14:57:01    0    model        Projection = [Albers]
2015-09-10T14:57:01    0    model        Simplify = []
2015-09-10T14:57:01    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:57:01    0    model        Zoom/Pan = [False]
2015-09-10T14:57:01    0    model        Legend = [False]
2015-09-10T14:57:01    0    model        LegendPos = [Top Left]
2015-09-10T14:57:01    0    model        IncExtras = [False]
2015-09-10T14:57:01    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:57:01    0    model        IncPopup = [False]
2015-09-10T14:57:01    0    model        PopupPos = [Bubble]
2015-09-10T14:57:01    0    model        Popup = []
2015-09-10T14:57:01    0    model        IncViz = [False]
2015-09-10T14:57:01    0    model        Chart = [Line Chart]
2015-09-10T14:57:01    0    model        VizWidth = [240]
2015-09-10T14:57:01    0    model        DataRanges = []
2015-09-10T14:57:01    0    model        Labels = []
2015-09-10T14:57:01    0    model EXPORT copying folders and files
2015-09-10T14:57:01    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:57:01    0    model Adding field: d3Css
2015-09-10T14:57:01    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:57:01    0    model setSingleSymbol
2015-09-10T14:57:01    0    model Filter: 
2015-09-10T14:57:01    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145701\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145701\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:57:02    0    winHelper topojson result 
            bounds: 99.64628906250002 0.8619628906250227 119.2663085937501 7.351660156250006 (spherical)
            pre-quantization: 2.18m (0.0000196Â°) 0.722m (0.00000649Â°)
            topology: 9 arcs, 509 points
            post-quantization: 218m (0.00196Â°) 72.2m (0.000649Â°)
            prune: retained 9 / 9 arcs (100%)
            
2015-09-10T14:57:02    0    model d3.geo.albers()
                  .center([0, 4])
                  .rotate([109.0, 0])
                  .parallels([0, 8])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:57:02    0    model EXPORT complete =========================================================
2015-09-10T14:58:02    0    model 2.10.1-Pisa
2015-09-10T14:58:02    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:58:02    0    topo Windows
2015-09-10T14:58:02    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:58:02    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:58:02    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:58:16    0    model EXPORT start ==================================================
2015-09-10T14:58:16    0    model        Title = [Mexico]
2015-09-10T14:58:16    0    model        Header = [False]
2015-09-10T14:58:16    0    model        Width = [800]
2015-09-10T14:58:16    0    model        Height = [600]
2015-09-10T14:58:16    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:58:16    0    model        IDField = [ID]
2015-09-10T14:58:16    0    model        Projection = [Albers]
2015-09-10T14:58:16    0    model        Simplify = []
2015-09-10T14:58:16    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:58:16    0    model        Zoom/Pan = [False]
2015-09-10T14:58:16    0    model        Legend = [False]
2015-09-10T14:58:16    0    model        LegendPos = [Top Left]
2015-09-10T14:58:16    0    model        IncExtras = [False]
2015-09-10T14:58:16    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:58:16    0    model        IncPopup = [False]
2015-09-10T14:58:16    0    model        PopupPos = [Bubble]
2015-09-10T14:58:16    0    model        Popup = []
2015-09-10T14:58:16    0    model        IncViz = [False]
2015-09-10T14:58:16    0    model        Chart = [Line Chart]
2015-09-10T14:58:16    0    model        VizWidth = [240]
2015-09-10T14:58:16    0    model        DataRanges = []
2015-09-10T14:58:16    0    model        Labels = []
2015-09-10T14:58:16    0    model EXPORT copying folders and files
2015-09-10T14:58:16    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:58:16    0    model Adding field: d3Css
2015-09-10T14:58:16    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:58:16    0    model setSingleSymbol
2015-09-10T14:58:16    0    model Filter: 
2015-09-10T14:58:16    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145816\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145816\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:58:16    0    winHelper topojson result 
            bounds: -118.40136718749997 14.545410156249986 -86.69628906249997 32.71533203125003 (spherical)
            pre-quantization: 3.53m (0.0000317Â°) 2.02m (0.0000182Â°)
            topology: 16 arcs, 1015 points
            post-quantization: 353m (0.00317Â°) 202m (0.00182Â°)
            prune: retained 16 / 16 arcs (100%)
            
2015-09-10T14:58:16    0    model d3.geo.albers()
                  .center([0, 23])
                  .rotate([102.0, 0])
                  .parallels([14, 33])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:58:16    0    model EXPORT complete =========================================================
2015-09-10T14:58:43    0    model 2.10.1-Pisa
2015-09-10T14:58:43    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:58:43    0    topo Windows
2015-09-10T14:58:43    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:58:43    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:58:43    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:58:57    0    model EXPORT start ==================================================
2015-09-10T14:58:57    0    model        Title = [Morocco]
2015-09-10T14:58:57    0    model        Header = [False]
2015-09-10T14:58:57    0    model        Width = [800]
2015-09-10T14:58:57    0    model        Height = [600]
2015-09-10T14:58:57    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:58:57    0    model        IDField = [ID]
2015-09-10T14:58:57    0    model        Projection = [Albers]
2015-09-10T14:58:57    0    model        Simplify = []
2015-09-10T14:58:57    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:58:57    0    model        Zoom/Pan = [False]
2015-09-10T14:58:57    0    model        Legend = [False]
2015-09-10T14:58:57    0    model        LegendPos = [Top Left]
2015-09-10T14:58:57    0    model        IncExtras = [False]
2015-09-10T14:58:57    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:58:57    0    model        IncPopup = [False]
2015-09-10T14:58:57    0    model        PopupPos = [Bubble]
2015-09-10T14:58:57    0    model        Popup = []
2015-09-10T14:58:57    0    model        IncViz = [False]
2015-09-10T14:58:57    0    model        Chart = [Line Chart]
2015-09-10T14:58:57    0    model        VizWidth = [240]
2015-09-10T14:58:57    0    model        DataRanges = []
2015-09-10T14:58:57    0    model        Labels = []
2015-09-10T14:58:57    0    model EXPORT copying folders and files
2015-09-10T14:58:57    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:58:57    0    model Adding field: d3Css
2015-09-10T14:58:57    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:58:57    0    model setSingleSymbol
2015-09-10T14:58:57    0    model Filter: 
2015-09-10T14:58:57    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145857\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145857\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:58:57    0    winHelper topojson result 
            bounds: -17.003076171874937 21.420703125000017 -1.0655273437499488 35.929882812499955 (spherical)
            pre-quantization: 1.77m (0.0000159Â°) 1.61m (0.0000145Â°)
            topology: 1 arcs, 368 points
            post-quantization: 177m (0.00159Â°) 161m (0.00145Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:58:57    0    model d3.geo.albers()
                  .center([0, 28])
                  .rotate([9.0, 0])
                  .parallels([21, 36])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:58:57    0    model EXPORT complete =========================================================
2015-09-10T14:59:27    0    model 2.10.1-Pisa
2015-09-10T14:59:27    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T14:59:27    0    topo Windows
2015-09-10T14:59:27    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T14:59:27    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T14:59:27    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T14:59:45    0    model EXPORT start ==================================================
2015-09-10T14:59:45    0    model        Title = [Namibia]
2015-09-10T14:59:45    0    model        Header = [False]
2015-09-10T14:59:45    0    model        Width = [800]
2015-09-10T14:59:45    0    model        Height = [600]
2015-09-10T14:59:45    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T14:59:45    0    model        IDField = [ID]
2015-09-10T14:59:45    0    model        Projection = [Albers]
2015-09-10T14:59:45    0    model        Simplify = []
2015-09-10T14:59:45    0    model        Output = [D:\Downloads\Temp]
2015-09-10T14:59:45    0    model        Zoom/Pan = [False]
2015-09-10T14:59:45    0    model        Legend = [False]
2015-09-10T14:59:45    0    model        LegendPos = [Top Left]
2015-09-10T14:59:45    0    model        IncExtras = [False]
2015-09-10T14:59:45    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T14:59:45    0    model        IncPopup = [False]
2015-09-10T14:59:45    0    model        PopupPos = [Bubble]
2015-09-10T14:59:45    0    model        Popup = []
2015-09-10T14:59:45    0    model        IncViz = [False]
2015-09-10T14:59:45    0    model        Chart = [Line Chart]
2015-09-10T14:59:45    0    model        VizWidth = [240]
2015-09-10T14:59:45    0    model        DataRanges = []
2015-09-10T14:59:45    0    model        Labels = []
2015-09-10T14:59:45    0    model EXPORT copying folders and files
2015-09-10T14:59:45    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T14:59:45    0    model Adding field: d3Css
2015-09-10T14:59:45    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T14:59:45    0    model setSingleSymbol
2015-09-10T14:59:45    0    model Filter: 
2015-09-10T14:59:45    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910145945\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910145945\shp\ne_50m_admin_0_countries.shp
2015-09-10T14:59:46    0    winHelper topojson result 
            bounds: 11.7216796875 -28.938769531250003 25.2587890625 -16.96767578125001 (spherical)
            pre-quantization: 1.51m (0.0000135Â°) 1.33m (0.0000120Â°)
            topology: 1 arcs, 235 points
            post-quantization: 151m (0.00135Â°) 133m (0.00120Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T14:59:46    0    model d3.geo.albers()
                  .center([0, -22])
                  .rotate([18.0, 0])
                  .parallels([-29, -16])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T14:59:46    0    model EXPORT complete =========================================================
2015-09-10T15:00:20    0    model 2.10.1-Pisa
2015-09-10T15:00:20    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T15:00:20    0    topo Windows
2015-09-10T15:00:20    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T15:00:20    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T15:00:20    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T15:00:35    0    model EXPORT start ==================================================
2015-09-10T15:00:35    0    model        Title = [New Zealand]
2015-09-10T15:00:35    0    model        Header = [False]
2015-09-10T15:00:35    0    model        Width = [800]
2015-09-10T15:00:35    0    model        Height = [600]
2015-09-10T15:00:35    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T15:00:35    0    model        IDField = [ID]
2015-09-10T15:00:35    0    model        Projection = [Albers]
2015-09-10T15:00:35    0    model        Simplify = []
2015-09-10T15:00:35    0    model        Output = [D:\Downloads\Temp]
2015-09-10T15:00:35    0    model        Zoom/Pan = [False]
2015-09-10T15:00:35    0    model        Legend = [False]
2015-09-10T15:00:35    0    model        LegendPos = [Top Left]
2015-09-10T15:00:35    0    model        IncExtras = [False]
2015-09-10T15:00:35    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T15:00:35    0    model        IncPopup = [False]
2015-09-10T15:00:35    0    model        PopupPos = [Bubble]
2015-09-10T15:00:35    0    model        Popup = []
2015-09-10T15:00:35    0    model        IncViz = [False]
2015-09-10T15:00:35    0    model        Chart = [Line Chart]
2015-09-10T15:00:35    0    model        VizWidth = [240]
2015-09-10T15:00:35    0    model        DataRanges = []
2015-09-10T15:00:35    0    model        Labels = []
2015-09-10T15:00:35    0    model EXPORT copying folders and files
2015-09-10T15:00:35    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T15:00:35    0    model Adding field: d3Css
2015-09-10T15:00:35    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T15:00:35    0    model setSingleSymbol
2015-09-10T15:00:35    0    model Filter: 
2015-09-10T15:00:35    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910150035\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910150035\shp\ne_50m_admin_0_countries.shp
2015-09-10T15:00:35    0    winHelper topojson result 
            bounds: -176.84765625000003 -52.570312499999964 178.53623046875006 -8.546484374999949 (spherical)
            pre-quantization: 39.5m (0.000355Â°) 4.90m (0.0000440Â°)
            topology: 13 arcs, 775 points
            post-quantization: 3.952km (0.0355Â°) 490m (0.00440Â°)
            prune: retained 12 / 13 arcs (92%)
            
2015-09-10T15:00:35    0    model d3.geo.albers()
                  .center([0, -30])
                  .rotate([0.0, 0])
                  .parallels([-53, -8])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T15:00:35    0    model EXPORT complete =========================================================
2015-09-10T19:11:14    0    model 2.10.1-Pisa
2015-09-10T19:11:14    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:11:14    0    topo Windows
2015-09-10T19:11:14    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:11:14    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:11:14    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:11:28    0    model EXPORT start ==================================================
2015-09-10T19:11:28    0    model        Title = [Peru]
2015-09-10T19:11:28    0    model        Header = [False]
2015-09-10T19:11:28    0    model        Width = [800]
2015-09-10T19:11:28    0    model        Height = [600]
2015-09-10T19:11:28    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:11:28    0    model        IDField = [ID]
2015-09-10T19:11:28    0    model        Projection = [Albers]
2015-09-10T19:11:28    0    model        Simplify = []
2015-09-10T19:11:28    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:11:28    0    model        Zoom/Pan = [False]
2015-09-10T19:11:28    0    model        Legend = [False]
2015-09-10T19:11:28    0    model        LegendPos = [Top Left]
2015-09-10T19:11:28    0    model        IncExtras = [False]
2015-09-10T19:11:28    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:11:28    0    model        IncPopup = [False]
2015-09-10T19:11:28    0    model        PopupPos = [Bubble]
2015-09-10T19:11:28    0    model        Popup = []
2015-09-10T19:11:28    0    model        IncViz = [False]
2015-09-10T19:11:28    0    model        Chart = [Line Chart]
2015-09-10T19:11:28    0    model        VizWidth = [240]
2015-09-10T19:11:28    0    model        DataRanges = []
2015-09-10T19:11:28    0    model        Labels = []
2015-09-10T19:11:28    0    model EXPORT copying folders and files
2015-09-10T19:11:28    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:11:28    0    model Adding field: d3Css
2015-09-10T19:11:28    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:11:28    0    model setSingleSymbol
2015-09-10T19:11:28    0    model Filter: 
2015-09-10T19:11:29    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910191128\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910191128\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:11:29    0    winHelper topojson result 
            bounds: -81.33662109375 -18.34560546875001 -68.68525390625 -0.041748046875 (spherical)
            pre-quantization: 1.41m (0.0000127Â°) 2.04m (0.0000183Â°)
            topology: 1 arcs, 589 points
            post-quantization: 141m (0.00127Â°) 204m (0.00183Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T19:11:29    0    model d3.geo.albers()
                  .center([0, -9])
                  .rotate([75.0, 0])
                  .parallels([-19, 0])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:11:29    0    model EXPORT complete =========================================================
2015-09-10T19:11:56    0    model 2.10.1-Pisa
2015-09-10T19:11:56    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:11:56    0    topo Windows
2015-09-10T19:11:56    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:11:56    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:11:56    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:12:10    0    model EXPORT start ==================================================
2015-09-10T19:12:10    0    model        Title = [Poland]
2015-09-10T19:12:10    0    model        Header = [False]
2015-09-10T19:12:10    0    model        Width = [800]
2015-09-10T19:12:10    0    model        Height = [600]
2015-09-10T19:12:10    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:12:10    0    model        IDField = [ID]
2015-09-10T19:12:10    0    model        Projection = [Albers]
2015-09-10T19:12:10    0    model        Simplify = []
2015-09-10T19:12:10    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:12:10    0    model        Zoom/Pan = [False]
2015-09-10T19:12:10    0    model        Legend = [False]
2015-09-10T19:12:10    0    model        LegendPos = [Top Left]
2015-09-10T19:12:10    0    model        IncExtras = [False]
2015-09-10T19:12:10    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:12:10    0    model        IncPopup = [False]
2015-09-10T19:12:10    0    model        PopupPos = [Bubble]
2015-09-10T19:12:10    0    model        Popup = []
2015-09-10T19:12:10    0    model        IncViz = [False]
2015-09-10T19:12:10    0    model        Chart = [Line Chart]
2015-09-10T19:12:10    0    model        VizWidth = [240]
2015-09-10T19:12:10    0    model        DataRanges = []
2015-09-10T19:12:10    0    model        Labels = []
2015-09-10T19:12:10    0    model EXPORT copying folders and files
2015-09-10T19:12:10    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:12:10    0    model Adding field: d3Css
2015-09-10T19:12:10    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:12:10    0    model setSingleSymbol
2015-09-10T19:12:10    0    model Filter: 
2015-09-10T19:12:11    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910191210\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910191210\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:12:11    0    winHelper topojson result 
            bounds: 14.128613281250011 49.020751953125 24.105761718750017 54.838183593749996 (spherical)
            pre-quantization: 1.11m (0.00000998Â°) 0.647m (0.00000582Â°)
            topology: 1 arcs, 316 points
            post-quantization: 111m (0.000998Â°) 64.7m (0.000582Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T19:12:11    0    model d3.geo.albers()
                  .center([0, 51])
                  .rotate([19.0, 0])
                  .parallels([49, 55])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:12:11    0    model EXPORT complete =========================================================
2015-09-10T19:12:37    0    model 2.10.1-Pisa
2015-09-10T19:12:37    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:12:37    0    topo Windows
2015-09-10T19:12:37    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:12:37    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:12:37    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:12:49    0    model EXPORT start ==================================================
2015-09-10T19:12:49    0    model        Title = [Qatar]
2015-09-10T19:12:49    0    model        Header = [False]
2015-09-10T19:12:49    0    model        Width = [800]
2015-09-10T19:12:49    0    model        Height = [600]
2015-09-10T19:12:49    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:12:49    0    model        IDField = [ID]
2015-09-10T19:12:49    0    model        Projection = [Albers]
2015-09-10T19:12:49    0    model        Simplify = []
2015-09-10T19:12:49    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:12:49    0    model        Zoom/Pan = [False]
2015-09-10T19:12:49    0    model        Legend = [False]
2015-09-10T19:12:49    0    model        LegendPos = [Top Left]
2015-09-10T19:12:49    0    model        IncExtras = [False]
2015-09-10T19:12:49    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:12:49    0    model        IncPopup = [False]
2015-09-10T19:12:49    0    model        PopupPos = [Bubble]
2015-09-10T19:12:49    0    model        Popup = []
2015-09-10T19:12:49    0    model        IncViz = [False]
2015-09-10T19:12:49    0    model        Chart = [Line Chart]
2015-09-10T19:12:49    0    model        VizWidth = [240]
2015-09-10T19:12:49    0    model        DataRanges = []
2015-09-10T19:12:49    0    model        Labels = []
2015-09-10T19:12:49    0    model EXPORT copying folders and files
2015-09-10T19:12:49    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:12:49    0    model Adding field: d3Css
2015-09-10T19:12:49    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:12:49    0    model setSingleSymbol
2015-09-10T19:12:49    0    model Filter: 
2015-09-10T19:12:50    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910191249\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910191249\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:12:50    0    winHelper topojson result 
            bounds: 50.75458984375001 24.564648437499997 51.60888671875 26.153271484374997 (spherical)
            pre-quantization: 0.0950m (8.54e-7Â°) 0.177m (0.00000159Â°)
            topology: 1 arcs, 34 points
            post-quantization: 9.50m (0.0000854Â°) 17.7m (0.000159Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T19:12:50    0    model d3.geo.albers()
                  .center([0, 25])
                  .rotate([51.0, 0])
                  .parallels([24, 27])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:12:50    0    model EXPORT complete =========================================================
2015-09-10T19:14:06    0    model 2.10.1-Pisa
2015-09-10T19:14:06    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:14:06    0    topo Windows
2015-09-10T19:14:06    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:14:06    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:14:06    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:14:22    0    model EXPORT start ==================================================
2015-09-10T19:14:22    0    model        Title = [Russia]
2015-09-10T19:14:22    0    model        Header = [False]
2015-09-10T19:14:22    0    model        Width = [800]
2015-09-10T19:14:22    0    model        Height = [600]
2015-09-10T19:14:22    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:14:22    0    model        IDField = [ID]
2015-09-10T19:14:22    0    model        Projection = [Albers]
2015-09-10T19:14:22    0    model        Simplify = []
2015-09-10T19:14:22    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:14:22    0    model        Zoom/Pan = [False]
2015-09-10T19:14:22    0    model        Legend = [False]
2015-09-10T19:14:22    0    model        LegendPos = [Top Left]
2015-09-10T19:14:22    0    model        IncExtras = [False]
2015-09-10T19:14:22    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:14:22    0    model        IncPopup = [False]
2015-09-10T19:14:22    0    model        PopupPos = [Bubble]
2015-09-10T19:14:22    0    model        Popup = []
2015-09-10T19:14:22    0    model        IncViz = [False]
2015-09-10T19:14:22    0    model        Chart = [Line Chart]
2015-09-10T19:14:22    0    model        VizWidth = [240]
2015-09-10T19:14:22    0    model        DataRanges = []
2015-09-10T19:14:22    0    model        Labels = []
2015-09-10T19:14:22    0    model EXPORT copying folders and files
2015-09-10T19:14:22    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:14:22    0    model Adding field: d3Css
2015-09-10T19:14:22    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:14:22    0    model setSingleSymbol
2015-09-10T19:14:22    0    model Filter: 
2015-09-10T19:14:22    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910191422\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910191422\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:14:22    0    winHelper topojson result 
            bounds: -180 41.19926757812502 180 81.85419921874998 (spherical)
            pre-quantization: 40.0m (0.000360Â°) 4.52m (0.0000407Â°)
            topology: 98 arcs, 7354 points
            post-quantization: 4.003km (0.0360Â°) 452m (0.00407Â°)
            prune: retained 98 / 98 arcs (100%)
            
2015-09-10T19:14:22    0    model d3.geo.albers()
                  .center([0, 61])
                  .rotate([0.0, 0])
                  .parallels([41, 82])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:14:22    0    model EXPORT complete =========================================================
2015-09-10T19:14:53    0    model 2.10.1-Pisa
2015-09-10T19:14:53    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:14:53    0    topo Windows
2015-09-10T19:14:53    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:14:53    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:14:53    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:15:09    0    model EXPORT start ==================================================
2015-09-10T19:15:09    0    model        Title = [Singapore]
2015-09-10T19:15:09    0    model        Header = [False]
2015-09-10T19:15:09    0    model        Width = [800]
2015-09-10T19:15:09    0    model        Height = [600]
2015-09-10T19:15:09    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:15:09    0    model        IDField = [ID]
2015-09-10T19:15:09    0    model        Projection = [Albers]
2015-09-10T19:15:09    0    model        Simplify = []
2015-09-10T19:15:09    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:15:09    0    model        Zoom/Pan = [False]
2015-09-10T19:15:09    0    model        Legend = [False]
2015-09-10T19:15:09    0    model        LegendPos = [Top Left]
2015-09-10T19:15:09    0    model        IncExtras = [False]
2015-09-10T19:15:09    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:15:09    0    model        IncPopup = [False]
2015-09-10T19:15:09    0    model        PopupPos = [Bubble]
2015-09-10T19:15:09    0    model        Popup = []
2015-09-10T19:15:09    0    model        IncViz = [False]
2015-09-10T19:15:09    0    model        Chart = [Line Chart]
2015-09-10T19:15:09    0    model        VizWidth = [240]
2015-09-10T19:15:09    0    model        DataRanges = []
2015-09-10T19:15:09    0    model        Labels = []
2015-09-10T19:15:09    0    model EXPORT copying folders and files
2015-09-10T19:15:09    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:15:09    0    model Adding field: d3Css
2015-09-10T19:15:09    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:15:09    0    model setSingleSymbol
2015-09-10T19:15:09    0    model Filter: 
2015-09-10T19:15:09    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910191509\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910191509\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:15:09    0    winHelper topojson result 
            bounds: 103.65019531249999 1.265380859375 103.99638671874999 1.4470703124999886 (spherical)
            pre-quantization: 0.0385m (3.46e-7Â°) 0.0202m (1.82e-7Â°)
            topology: 1 arcs, 9 points
            post-quantization: 3.85m (0.0000346Â°) 2.02m (0.0000182Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T19:15:09    0    model d3.geo.albers()
                  .center([0, 1])
                  .rotate([103.0, 0])
                  .parallels([1, 2])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:15:10    0    model EXPORT complete =========================================================
2015-09-10T19:24:23    0    model 2.10.1-Pisa
2015-09-10T19:24:23    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:24:23    0    topo Windows
2015-09-10T19:24:23    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:24:23    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:24:23    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:24:37    0    model EXPORT start ==================================================
2015-09-10T19:24:37    0    model        Title = [Somalia]
2015-09-10T19:24:37    0    model        Header = [False]
2015-09-10T19:24:37    0    model        Width = [800]
2015-09-10T19:24:37    0    model        Height = [600]
2015-09-10T19:24:37    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:24:37    0    model        IDField = [ID]
2015-09-10T19:24:37    0    model        Projection = [Albers]
2015-09-10T19:24:37    0    model        Simplify = []
2015-09-10T19:24:37    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:24:37    0    model        Zoom/Pan = [False]
2015-09-10T19:24:37    0    model        Legend = [False]
2015-09-10T19:24:37    0    model        LegendPos = [Top Left]
2015-09-10T19:24:37    0    model        IncExtras = [False]
2015-09-10T19:24:37    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:24:37    0    model        IncPopup = [False]
2015-09-10T19:24:37    0    model        PopupPos = [Bubble]
2015-09-10T19:24:37    0    model        Popup = []
2015-09-10T19:24:37    0    model        IncViz = [False]
2015-09-10T19:24:37    0    model        Chart = [Line Chart]
2015-09-10T19:24:37    0    model        VizWidth = [240]
2015-09-10T19:24:37    0    model        DataRanges = []
2015-09-10T19:24:37    0    model        Labels = []
2015-09-10T19:24:37    0    model EXPORT copying folders and files
2015-09-10T19:24:37    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:24:38    0    model Adding field: d3Css
2015-09-10T19:24:38    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:24:38    0    model setSingleSymbol
2015-09-10T19:24:38    0    model Filter: 
2015-09-10T19:24:38    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910192437\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910192437\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:24:38    0    winHelper topojson result 
            bounds: 40.964453125000006 -1.6953125 51.390234375000006 11.983691406249989 (spherical)
            pre-quantization: 1.16m (0.0000104Â°) 1.52m (0.0000137Â°)
            topology: 1 arcs, 143 points
            post-quantization: 116m (0.00104Â°) 152m (0.00137Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T19:24:38    0    model d3.geo.albers()
                  .center([0, 5])
                  .rotate([46.0, 0])
                  .parallels([-2, 12])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:24:38    0    model EXPORT complete =========================================================
2015-09-10T19:26:06    0    model 2.10.1-Pisa
2015-09-10T19:26:06    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:26:06    0    topo Windows
2015-09-10T19:26:06    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:26:06    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:26:06    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:26:20    0    model EXPORT start ==================================================
2015-09-10T19:26:20    0    model        Title = [Sweden]
2015-09-10T19:26:20    0    model        Header = [False]
2015-09-10T19:26:20    0    model        Width = [800]
2015-09-10T19:26:20    0    model        Height = [600]
2015-09-10T19:26:20    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:26:20    0    model        IDField = [ID]
2015-09-10T19:26:20    0    model        Projection = [Albers]
2015-09-10T19:26:20    0    model        Simplify = []
2015-09-10T19:26:20    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:26:20    0    model        Zoom/Pan = [False]
2015-09-10T19:26:20    0    model        Legend = [False]
2015-09-10T19:26:20    0    model        LegendPos = [Top Left]
2015-09-10T19:26:20    0    model        IncExtras = [False]
2015-09-10T19:26:20    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:26:20    0    model        IncPopup = [False]
2015-09-10T19:26:20    0    model        PopupPos = [Bubble]
2015-09-10T19:26:20    0    model        Popup = []
2015-09-10T19:26:20    0    model        IncViz = [False]
2015-09-10T19:26:20    0    model        Chart = [Line Chart]
2015-09-10T19:26:20    0    model        VizWidth = [240]
2015-09-10T19:26:20    0    model        DataRanges = []
2015-09-10T19:26:20    0    model        Labels = []
2015-09-10T19:26:20    0    model EXPORT copying folders and files
2015-09-10T19:26:20    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:26:21    0    model Adding field: d3Css
2015-09-10T19:26:21    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:26:21    0    model setSingleSymbol
2015-09-10T19:26:21    0    model Filter: 
2015-09-10T19:26:21    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910192620\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910192620\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:26:21    0    winHelper topojson result 
            bounds: 11.14716796875004 55.34638671875004 24.15546875000004 69.036865234375 (spherical)
            pre-quantization: 1.45m (0.0000130Â°) 1.52m (0.0000137Â°)
            topology: 6 arcs, 593 points
            post-quantization: 145m (0.00130Â°) 152m (0.00137Â°)
            prune: retained 6 / 6 arcs (100%)
            
2015-09-10T19:26:21    0    model d3.geo.albers()
                  .center([0, 62])
                  .rotate([17.0, 0])
                  .parallels([55, 70])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:26:21    0    model EXPORT complete =========================================================
2015-09-10T19:27:00    0    model 2.10.1-Pisa
2015-09-10T19:27:00    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:27:00    0    topo Windows
2015-09-10T19:27:00    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:27:00    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:27:00    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:27:14    0    model EXPORT start ==================================================
2015-09-10T19:27:14    0    model        Title = [Tonga]
2015-09-10T19:27:14    0    model        Header = [False]
2015-09-10T19:27:14    0    model        Width = [800]
2015-09-10T19:27:14    0    model        Height = [600]
2015-09-10T19:27:14    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:27:14    0    model        IDField = [ID]
2015-09-10T19:27:14    0    model        Projection = [Albers]
2015-09-10T19:27:14    0    model        Simplify = []
2015-09-10T19:27:14    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:27:14    0    model        Zoom/Pan = [False]
2015-09-10T19:27:14    0    model        Legend = [False]
2015-09-10T19:27:14    0    model        LegendPos = [Top Left]
2015-09-10T19:27:14    0    model        IncExtras = [False]
2015-09-10T19:27:14    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:27:14    0    model        IncPopup = [False]
2015-09-10T19:27:14    0    model        PopupPos = [Bubble]
2015-09-10T19:27:14    0    model        Popup = []
2015-09-10T19:27:14    0    model        IncViz = [False]
2015-09-10T19:27:14    0    model        Chart = [Line Chart]
2015-09-10T19:27:14    0    model        VizWidth = [240]
2015-09-10T19:27:14    0    model        DataRanges = []
2015-09-10T19:27:14    0    model        Labels = []
2015-09-10T19:27:14    0    model EXPORT copying folders and files
2015-09-10T19:27:14    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:27:14    0    model Adding field: d3Css
2015-09-10T19:27:14    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:27:14    0    model setSingleSymbol
2015-09-10T19:27:14    0    model Filter: 
2015-09-10T19:27:14    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910192714\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910192714\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:27:14    0    winHelper topojson result 
            bounds: -175.36235351562496 -21.450585937500037 -173.92187500000003 -18.565332031250023 (spherical)
            pre-quantization: 0.160m (0.00000144Â°) 0.321m (0.00000289Â°)
            topology: 3 arcs, 32 points
            post-quantization: 16.0m (0.000144Â°) 32.1m (0.000289Â°)
            prune: retained 3 / 3 arcs (100%)
            
2015-09-10T19:27:14    0    model d3.geo.albers()
                  .center([0, -20])
                  .rotate([174.0, 0])
                  .parallels([-22, -18])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:27:14    0    model EXPORT complete =========================================================
2015-09-10T19:27:43    0    model 2.10.1-Pisa
2015-09-10T19:27:43    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:27:43    0    topo Windows
2015-09-10T19:27:43    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:27:43    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:27:43    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:28:35    0    model 2.10.1-Pisa
2015-09-10T19:28:35    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:28:35    0    topo Windows
2015-09-10T19:28:35    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:28:35    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:28:35    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:28:56    0    model EXPORT start ==================================================
2015-09-10T19:28:56    0    model        Title = [Yemen]
2015-09-10T19:28:56    0    model        Header = [False]
2015-09-10T19:28:56    0    model        Width = [800]
2015-09-10T19:28:56    0    model        Height = [600]
2015-09-10T19:28:56    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:28:56    0    model        IDField = [ID]
2015-09-10T19:28:56    0    model        Projection = [Albers]
2015-09-10T19:28:56    0    model        Simplify = []
2015-09-10T19:28:56    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:28:56    0    model        Zoom/Pan = [False]
2015-09-10T19:28:56    0    model        Legend = [False]
2015-09-10T19:28:56    0    model        LegendPos = [Top Left]
2015-09-10T19:28:56    0    model        IncExtras = [False]
2015-09-10T19:28:56    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:28:56    0    model        IncPopup = [False]
2015-09-10T19:28:56    0    model        PopupPos = [Bubble]
2015-09-10T19:28:56    0    model        Popup = []
2015-09-10T19:28:56    0    model        IncViz = [False]
2015-09-10T19:28:56    0    model        Chart = [Line Chart]
2015-09-10T19:28:56    0    model        VizWidth = [240]
2015-09-10T19:28:56    0    model        DataRanges = []
2015-09-10T19:28:56    0    model        Labels = []
2015-09-10T19:28:56    0    model EXPORT copying folders and files
2015-09-10T19:28:56    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:28:56    0    model Adding field: d3Css
2015-09-10T19:28:56    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:28:56    0    model setSingleSymbol
2015-09-10T19:28:56    0    model Filter: 
2015-09-10T19:28:56    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910192856\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910192856\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:28:56    0    winHelper topojson result 
            bounds: 42.5490234375001 12.318994140624994 54.511132812499994 18.996142578125074 (spherical)
            pre-quantization: 1.33m (0.0000120Â°) 0.743m (0.00000668Â°)
            topology: 5 arcs, 225 points
            post-quantization: 133m (0.00120Â°) 74.3m (0.000668Â°)
            prune: retained 5 / 5 arcs (100%)
            
2015-09-10T19:28:56    0    model d3.geo.albers()
                  .center([0, 15])
                  .rotate([48.0, 0])
                  .parallels([12, 19])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:28:56    0    model EXPORT complete =========================================================
2015-09-10T19:29:32    0    model 2.10.1-Pisa
2015-09-10T19:29:32    0    model 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)]
2015-09-10T19:29:32    0    topo Windows
2015-09-10T19:29:32    0    winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-09-10T19:29:32    0    winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm;C:\Program Files\QGIS Wien\bin;C:\Program Files\QGIS Wien\apps\qgis\bin
2015-09-10T19:29:32    0    winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-09-10T19:29:53    0    model EXPORT start ==================================================
2015-09-10T19:29:53    0    model        Title = [Zimbabwe]
2015-09-10T19:29:53    0    model        Header = [False]
2015-09-10T19:29:53    0    model        Width = [800]
2015-09-10T19:29:53    0    model        Height = [600]
2015-09-10T19:29:53    0    model        Main layer = [ne_50m_admin_0_countries]
2015-09-10T19:29:53    0    model        IDField = [ID]
2015-09-10T19:29:53    0    model        Projection = [Albers]
2015-09-10T19:29:53    0    model        Simplify = []
2015-09-10T19:29:53    0    model        Output = [D:\Downloads\Temp]
2015-09-10T19:29:53    0    model        Zoom/Pan = [False]
2015-09-10T19:29:53    0    model        Legend = [False]
2015-09-10T19:29:53    0    model        LegendPos = [Top Left]
2015-09-10T19:29:53    0    model        IncExtras = [False]
2015-09-10T19:29:53    0    model        Extras = [ne_50m_admin_0_countries]
2015-09-10T19:29:53    0    model        IncPopup = [False]
2015-09-10T19:29:53    0    model        PopupPos = [Bubble]
2015-09-10T19:29:53    0    model        Popup = []
2015-09-10T19:29:53    0    model        IncViz = [False]
2015-09-10T19:29:53    0    model        Chart = [Line Chart]
2015-09-10T19:29:53    0    model        VizWidth = [240]
2015-09-10T19:29:53    0    model        DataRanges = []
2015-09-10T19:29:53    0    model        Labels = []
2015-09-10T19:29:53    0    model EXPORT copying folders and files
2015-09-10T19:29:53    0    model EXPORT ne_50m_admin_0_countries
2015-09-10T19:29:53    0    model Adding field: d3Css
2015-09-10T19:29:53    0    model SINGLE: FILL SYMBOL (1 layers) color 0,0,0,255
2015-09-10T19:29:53    0    model setSingleSymbol
2015-09-10T19:29:53    0    model Filter: 
2015-09-10T19:29:53    0    winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o D:\Downloads\Temp\20150910192953\topo\ne50madmin0countries.json --id-property ID -p d3Css -- l0=D:\Downloads\Temp\20150910192953\shp\ne_50m_admin_0_countries.shp
2015-09-10T19:29:54    0    winHelper topojson result 
            bounds: 25.224023437500023 -22.40205078125001 33.00673828125002 -15.64306640625 (spherical)
            pre-quantization: 0.865m (0.00000778Â°) 0.752m (0.00000676Â°)
            topology: 1 arcs, 170 points
            post-quantization: 86.5m (0.000778Â°) 75.2m (0.000676Â°)
            prune: retained 1 / 1 arcs (100%)
            
2015-09-10T19:29:54    0    model d3.geo.albers()
                  .center([0, -19])
                  .rotate([29.0, 0])
                  .parallels([-23, -15])
                  .scale(1000)
                  .translate([width / 2, height / 2])
2015-09-10T19:29:54    0    model EXPORT complete =========================================================
'''

