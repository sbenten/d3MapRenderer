# -*- coding: utf-8 -*-
"""
/***************************************************************************
 d3MapRenderer
                                 A QGIS plugin
 Vector logic and data visualisation with the d3.js library.
                             -------------------
        begin                : 2015-06-17
        copyright            : (C) 2015 by Simon Benten
        email                : swbenten@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load d3MapRenderer class from file d3MapRenderer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .d3_Map import d3MapRenderer
    return d3MapRenderer(iface)
