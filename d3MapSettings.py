# -*- coding: utf-8 -*-
"""
/***************************************************************************
 d3MapSettings
                                 A QGIS plugin
 d3MapSettings
                              -------------------
        begin                : 2015-10-13
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Simon Benten
        email                : swbenten@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from d3MapSettings_dialog import d3MapSettingsDialog
import os.path

from settings import globalSettings
from qgis.PyQt.QtGui import *
import tempfile
from osHelp import osHelper

class d3MapSettings:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'd3MapRenderer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = d3MapSettingsDialog()
        self.settings = globalSettings()
        self.osHelp = osHelper()
        
    def changedOutput(self):
        """Perform validation when the output directory is altered"""
        self.validateOutput()

    def validateOutput(self):
        """Perform validation on the output directory"""
        result  = True
        if len(self.dlg.outputEdit.text()) == 0:
            result = False
        else:
            if os.path.exists(self.dlg.outputEdit.text()) == False:
                result = False
                
        if self.osHelp.isWindows == True:
            # Restriction on windows command call to ASCII only characters
            # Prevent input of Unicode characters here
            try:
                self.dlg.outputEdit.text().decode('ascii')
            except UnicodeEncodeError: 
                result = False

        if result == True:
            self.dlg.outputEdit.setStyleSheet('QLineEdit { background-color: #ffffff }')
        else:
            self.dlg.outputEdit.setStyleSheet('QLineEdit { background-color: #f6989d }')
            self.dlg.outputEdit.setFocus()
            
        return result
    
    def doShowFolderDialog(self):
        """Display a folder dialog for the output directory"""
        folder = self.dlg.outputEdit.text()
        if len(folder) == 0:
            # no previous folder specified, set to the os temporary directory
            folder =  tempfile.gettempdir()   
        folder = QFileDialog.getExistingDirectory(self.dlg, "Select Output Directory", folder, QFileDialog.ShowDirsOnly)
        if len(folder) > 0:
            self.dlg.outputEdit.setText(folder)
            
    def saveSettings(self):
        """Ok clicked run the process and close dialog"""       
        if self.validateOutput() == True:
            self.settings.setOutputPath(self.dlg.outputEdit.text())
            
            serverUrl = self.dlg.httpEdit.text()
            
            if serverUrl != "":
                if serverUrl.startswith("http://") == False and serverUrl.startswith("https://") == False:
                    serverUrl = "http://" + serverUrl
                if serverUrl.endswith("/") == False:
                    serverUrl = serverUrl + "/"   
                self.settings.setWebServerUrl(serverUrl)       
            
            self.closeDialog()

            
    def closeDialog(self):
        """Cancel clicked closed the dialog"""
        self.disposeUI()
        self.dlg.close()

    def run(self):
        """Run method that performs all the real work"""
        self.setupUI()

    def setupUI(self):
        """Show the dialog and bind events"""
        self.dlg.show()
        
        # Set UI state to match the model
        self.resetFields()
        
        # attach events
        self.dlg.outputEdit.textChanged.connect(self.changedOutput)
        self.dlg.outputButton.clicked.connect(self.doShowFolderDialog)
        
        # buttons
        self.dlg.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.closeDialog)
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.saveSettings) 
        
        # Run the dialog event loop
        self.dlg.exec_()
        
    def resetFields(self):
        """Reset the fields to the starting state"""
        self.dlg.httpEdit.setText(self.settings.webServerUrl())
        self.dlg.outputEdit.setText(self.settings.outputPath())


    def disposeUI(self):
        """Unbind events and reset state to match the model"""
        try:
            self.dlg.outputEdit.textChanged.disconnect()
            self.dlg.outputButton.clicked.disconnect()

            # buttons
            self.dlg.buttonBox.button(QDialogButtonBox.Cancel).clicked.disconnect()
            self.dlg.buttonBox.button(QDialogButtonBox.Ok).clicked.disconnect()
        except TypeError:
            pass
        
        self.resetFields()
        
        
        
