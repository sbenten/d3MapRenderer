import sys
import traceback
from qgis.core import *

class log:
    """Helper class for logging messages
    
    Currently only implements the QgsMessageLog but will allow extension 
    to another logger in the future, should the need arise"""  
    
    def __init__(self, name):
        """Constructor"""
        self.tag = "d3MapRenderer"
        self.className = name
        
    def info(self, message):
        """Log a message at the info level"""
        QgsMessageLog.logMessage(self.className + " " + message, self.tag, QgsMessageLog.INFO) 
       
    def error2(self):
        """Log a message at the error level""" 
        e_type, e_value, e_traceback = sys.exc_info()
        lines = traceback.format_exception(e_type, e_value, e_traceback)
  
        self.error("".join(" " + line for line in lines))
        
    def error(self, message):  
        """Log a message at the error level""" 
        QgsMessageLog.logMessage(self.className + " " + message, self.tag, QgsMessageLog.CRITICAL) 