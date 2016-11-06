import sys
import os
import platform
import locale
import codecs

from subprocess import *

from logger import log

class osHelper:
    """Helper class to check for topojson"""
    
    def __init__(self):
        """Constructor"""
        self.__logger = log(self.__class__.__name__)
        
        self.platform = platform.system()
        self.isWindows = False
        self.helper = linuxHelper()
                
        self.__logger.info(platform.system())
        
        if platform.system() == "Windows":
            self.isWindows = True
            self.helper = winHelper() 
                
class linuxHelper:
    """Linux OS class for performing topojson commands"""
        
    def __init__(self):
        """Constructor. Nothing special here"""
        self.__logger = log(self.__class__.__name__)
        self.topoVersion = 1
        
    def hasTopojson(self):
        """Does this OS have topojson installed?
        
        :returns: Whether the topojson is installed  
        :rtype: bool  
        """
        success = False
        
        try:
            result = check_output(["which", "topojson"])            
            self.__logger.info("which result " + result)             
            success = True             
        
        except CalledProcessError:            
            self.__logger.error2()           
        
        if sucess == False:    
            try:
                result = check_output(["which", "geo2topo"])            
                self.__logger.info("which result " + result)  
                self.topoVersion = 2           
                success = True             
            
            except CalledProcessError:            
                self.__logger.error2()  
            
        return success
    
    def output(self, folder, outFile, name, inFile, quantization, simplification):
        """Output the geojson file as topojson
        
        :param folder: Folder to output the topojson file.
            Assumed that this folder has been created outside of this class
        :type folder: str
        
        :param outFile: Name of the resulting topojson file. 
            ".json" will be added automatically as a suffix 
        :type outFile: str
        
        :param name: Name of the topojson object. 
        :type name: str        
        
        :param inFile: Path to the GeoJson file.
        :type inFile: str
        
        :param quantization: Maximum number of differentiable points along either dimension.
        :type quantization: str
        
        :param simplification: Precision threshold as string.
        :type simplification: str
              
        :returns: The message from topojson  
        :rtype: string         
        """
        result = ""

        args = []
        
        if self.topoVersion == 1:
            """Original topojson"""
            args.append("topojson")
            args.append("-o")
            args.append(os.path.join(folder, outFile + ".json"))        
            args.append("-p")
            
            if len(quantization) > 0:
                args.append("-q")
                args.append(quantization)
            if len(simplification) > 0:
                args.append("-s")
                args.append(simplification)
                
            args.append("--")
            args.append(name + "=" + inFile)
        
        if self.topoVersion == 2:    
            """New version of topojson is a subset of the original functionality
            as its been modularised. Now actually called goe2topo"""
            args.append("geo2topo")
            args.append(inFile) 
            args.append(">")
            args.append(name + "=")
            args.append(os.path.join(folder, outFile + ".json"))        
            args.append("-p")
            
            if len(quantization) > 0:
                args.append("-q")
                args.append(quantization)
            if len(simplification) > 0:
                args.append("-s")
                args.append(simplification)              
                  
        self.__logger.info(" ".join(args)) 
        
        result = check_output(args, stderr=STDOUT)
        
        self.__logger.info("topojson result " + result)              
            
        return result
    
class winHelper(linuxHelper):
    """Windows OS class for performing topojson commands
    
        Windows requires extra messing around to call topojson (or any other npm package) from python"""
    
    def __init__(self):
        """Constructor"""
        self.node = ""
        self.topojs = ""
        self.topoVersion = 1
        self.__logger = log(self.__class__.__name__) 
        self.reg = __import__("_winreg")     
    
    def hasTopojson(self):
        """TopoJson check in windows is a complicated mess
        
        :returns: Whether the topojson is installed  
        :rtype: bool  
        """
        
        nodeFound = self.getNodeJsPath()
        topoFound = False
        if nodeFound:
            # No point in doing this if nodeJS not installed, as the npm command will fail
            topoFound = self.getTopoJsonPath()
            
        return nodeFound and topoFound
    
    def output(self, folder, outFile, name, inFile, quantization, simplification):
        """Output the geojson file as topojson
        
        :param folder: Folder to output the topojson file.
            Assumed that this folder has been created outside of this class
        :type folder: str
        
        :param outFile: Name of the resulting topojson file. 
            ".json" will be added automatically as a suffix 
        :type outFile: str
        
        :param name: Name of the topojson object. 
        :type name: str
        
        :param inFile: Path to the GeoJson file.
        :type inFile: str
        
        :param quantization: Maximum number of differentiable points along either dimension.
        :type quantization: str
        
        :param simplification: Precision threshold as string.
        :type simplification: str
              
        :returns: The message from topojson  
        :rtype: string         
        """
        result = ""

        if self.hasTopojson() == True:
            args = []
            args.append(self.node)
            args.append(self.topojs)
            
            if self.topoVersion == 1:
                """Original topojson"""
                args.append("-o")
                args.append(os.path.join(folder, outFile + ".json"))        
                args.append("-p")
                
                if len(quantization) > 0:
                    args.append("-q")
                    args.append(quantization)
                if len(simplification) > 0:
                    args.append("-s")
                    args.append(simplification)
                    
                args.append("--")
                args.append(name + "=" + inFile)

            
            if self.topoVersion == 2:    
                """New version of topojson is a subset of the original functionality
                as its been modularised. Now actually called goe2topo"""
                args.append(inFile) 
                args.append(">")
                args.append(name + "=")
                args.append(os.path.join(folder, outFile + ".json"))        
                args.append("-p")
                
                if len(quantization) > 0:
                    args.append("-q")
                    args.append(quantization)
                if len(simplification) > 0:
                    args.append("-s")
                    args.append(simplification) 
            
            self.__logger.info(" ".join(args)) 
                 
            result = check_output(args, stderr=STDOUT, shell=True)
            
            self.__logger.info("topojson result \r\n" + result)               
            
        return result
    
    def getNodeJsPath(self):
        """Attempt to get the install location of nodejs"""
        
        # NodeJs could be installed anywhere and called anything so can't rely on 
        # Try the Current User InstallPath
        subname = os.path.normpath("Software/node.js")
        valName = "InstallPath"
        found = False
        try:
            # Query the registry...
            self.__logger.info("Query registry for " + os.path.join("HKEY_CURRENT_USER", subname, valName))
            subkey = self.reg.OpenKey(self.reg.HKEY_CURRENT_USER, subname)
            
            i = 0
            while 1:
                name, value, type = self.reg.EnumValue(subkey, i)
                if name == valName:
                    self.node = os.path.join(value, "node.exe")
                    self.__logger.info("node.js found at " + self.node)
                    found = True
                    break
                
                i += 1
        except WindowsError as e:
            self.__logger.error(e.args[1] + ": " + subname)
        
        if found == False:
            # Later versions of the Node.JS installer have removed the previous location 
            # in favour of the local machine  installed software  
            subname = os.path.normpath("SOFTWARE/node.js")
            try:
                # Query the registry...
                self.__logger.info("Query registry for " + os.path.join("HKEY_LOCAL_MACHINE", subname, valName))
                subkey = self.reg.OpenKey(self.reg.HKEY_LOCAL_MACHINE, subname)
                
                i = 0
                while 1:
                    name, value, type = self.reg.EnumValue(subkey, i)
                    if name == valName:
                        self.node = os.path.join(value, "node.exe")
                        self.__logger.info("node.js found at " + self.node)
                        found = True
                        break
                    
                    i += 1
            except WindowsError as e:
                self.__logger.error(e.args[1] + ": " + subname)                
                
                
        
        
        
        return found
        
    
    def getTopoJsonPath(self):
        """Attempt to get the topojson  package installation location"""
        
        # Node Package Manager could be installed anywhere
        # Look in the PATH user environment variable
        subname = "Environment"
        valName = "PATH"
        npm = os.path.normpath("/npm")
        topopkg = os.path.normpath("node_modules/topojson/bin/topojson")
        topopkg2 = os.path.normpath("node_modules/topojson/bin/geo2topo")
        found = False
        try:
            # Query the registry...
            self.__logger.info("Query registry for " + os.path.join("HKEY_CURRENT_USER", subname, valName))
            subkey = self.reg.OpenKey(self.reg.HKEY_CURRENT_USER, subname)
            
            i = 0
            while 1:
                name, value, type = self.reg.EnumValue(subkey, i)
                if name == valName:
                    self.__logger.info("User environment variables: " + value)
                    paths = value.split(";")
                    for p in paths:
                        # Is this the /npm value?
                        if p.endswith(npm):
                            temp = os.path.join(p, topopkg)
                            if os.path.isfile(temp) == True:
                                self.topojs = temp 
                                self.topoVersion = 1
                                self.__logger.info("topojson found at " + self.topojs)
                                found = True
                                break
                            else:
                                temp = os.path.join(p, topopkg2) 
                                if os.path.isfile(temp) == True:
                                    self.topojs = temp
                                    self.topoVersion = 2
                                    self.__logger.info("topojson found at " + self.topojs)
                                    found = True
                                    break
                
                i += 1
                
        except WindowsError as e:
            self.__logger.error(e.args[1] + ": " + subname)
            
        return found            