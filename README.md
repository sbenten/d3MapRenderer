d3 Map Renderer [![license](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/sbenten/d3MapRenderer/tree/master/LICENSE)
==


A python **QGIS** plugin to export of polygons, polylines and point vector layers from shapefiles to topojson for display within a web page using the [d3.js](http://d3js.org/) JavaScript library, with additional options of popup information, charts from [c3.js](http://c3js.org/) and a map legend.


Pre-requisites of [QGIS](http://www.qgis.org/en/site/) and the [Node.js](https://nodejs.org/) topojson package.


## Pre-requisites


Download and install [QGIS](https://www.qgis.org/en/site/forusers/download.html).


Download and install [Node.js](https://nodejs.org/download/).


Once Node.js is installed, you will need to install the topojson package which converts Geographic Information System shapefiles to d3's topojson format.  This can be done by opening a command prompt or terminal (depending on your operating system), and typing:


```
npm install -g topojson
```
This command downloads the topojson package and registers it for use on the command line.


d3 relies heavily on [JSON](https://en.wikipedia.org/wiki/JSON) files for loading data, and topojson is no different. To see the results of an export via this plugin you will also need a web server, as restrictions in modern web browsers prevent json files being loaded from the local file system. So if you want to view the results of the export before uploading to a website in the cloud (recomended), you will need a web server.


If you haven’t already got a web server already installed use [http-server] (https://www.npmjs.com/package/http-server) for Node.js. Install it by returning to that command line and typing:
```
npm install -g http-server
```
http-server is started and stopped via the command line, and it is as simple as changing to the directory where you are going to output your d3 maps (this will be the root of the local web site), and starting the server. For example, on Windows this would be the following two commands (obviously using your own directory path):
```
cd c:\Users\Simon\Documents
http-server
```
That wasn’t so bad was it? 


## Installation

Download from the QGIS plugin repository. Currently flagged as an experimental plugin.


If you want to try the bleeding edge version, [download the zip](https://github.com/sbenten/d3MapRenderer/archive/master.zip) direct from GitHub, and extract the contents into your QGIS python plugins directory (which on Windows is something along the lines of C:\Users\Simon\\.qgis2\python\plugins\). Rename the folder from d3MapRenderer-master to just d3MapRenderer and you will find the plugin listed along side the others in the QGIS plugin repository.   


## Logging issues and feature requests


The [issue](https://github.com/sbenten/d3MapRenderer/issues) log is to be used for reporting problems with the plugin and for feature requests and ideas. It is **not** a support forum. Nor is it the place to log problems with topojson, d3 or c3.


Before reporting an issue, please do the following:


1. Search for existing [issues](https://github.com/sbenten/d3MapRenderer/issues) to ensure you're not creating a duplicate.


1. When posting the issue, please use a descriptive title, include the plugin version and relevant details about what was trying to be achieved with the plugin. 


1. Also, please post the details from the Log Messages Panel within QGIS, and if possible a link to download the pertinent shapefiles. A sample of the log messages for the plugin:


```
2015-08-12T14:56:58 0 winHelper node.js found at C:\Program Files\nodejs\node.exe
2015-08-12T14:56:58 0 winHelper User environment variables: C:\Users\Simon\AppData\Roaming\npm
2015-08-12T14:56:58 0 winHelper topojson found at C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson
2015-08-12T15:00:50 0 model EXPORT start ==================================================
2015-08-12T15:00:50 0 model        Title = [English IMD]
2015-08-12T15:00:50 0 model        Header = [True]
2015-08-12T15:00:50 0 model        Width = [600]
2015-08-12T15:00:50 0 model        Height = [900]
2015-08-12T15:00:50 0 model        Main layer = [LSOA_2001_IMD]
2015-08-12T15:00:50 0 model        IDField = [LSOA01CD]
2015-08-12T15:00:50 0 model        Projection = [Albers]
2015-08-12T15:00:50 0 model        Simplify = [1e-9]
2015-08-12T15:00:50 0 model        Output = [D:\Downloads\Temp]
2015-08-12T15:00:50 0 model        Zoom/Pan = [True]
2015-08-12T15:00:50 0 model        Legend = [True]
2015-08-12T15:00:50 0 model        LegendPos = [Top Left]
2015-08-12T15:00:50 0 model        IncExtras = [True]
2015-08-12T15:00:50 0 model        Extras = [UK_IRE_POLY, LSOA_2001_IMD]
2015-08-12T15:00:50 0 model        IncPopup = [True]
2015-08-12T15:00:50 0 model        PopupPos = [Bubble]
2015-08-12T15:00:50 0 model        Popup = [<table>
<tr><td>GORNAME</td><td>{GORNAME}</td></tr>
<tr><td>LANAME</td><td>{LANAME}</td></tr>
<tr><td>LACODE</td><td>{LACODE}</td></tr>
</table><div id="chart" style="width: 240px; height: 240px"></div>]
2015-08-12T15:00:50 0 model        IncViz = [True]
2015-08-12T15:00:50 0 model        Chart = [Spline Chart]
2015-08-12T15:00:50 0 model        VizWidth = [240]
2015-08-12T15:00:50 0 model        DataRanges = [Overview:  OVRK2004   , OVRK2007   , OVRK2010   
Income:    INCRK2004  , INCRK2007  , INCRK2010  
Employment:EMPRK2004  , EMPRK2007  , EMPRK2010  
Health:    HLTHRK2004 , HLTHRK2007 , HLTHRK2010 
Education: EDRK2004   , EDRK2007   , EDRK2010   
Barriers to Housing and Services:HOURK2004  , HOUSRK2007 , HOUSRK2010 
Crime:     CRMRK2004  , CRMRK2007  , CRMRK2010  
Living Environment:LENVRK2004 , LENVRK2007 , LENVRK2010 
]
2015-08-12T15:00:50 0 model        Labels = [2004, 2007, 2010]
2015-08-12T15:00:50 0 model EXPORT copying folders and files
2015-08-12T15:00:50 0 model EXPORT UK_IRE_POLY
2015-08-12T15:00:51 0 model SINGLE: FILL SYMBOL (1 layers) color 217,217,217,255
2015-08-12T15:00:51 0 model setSingleSymbol
2015-08-12T15:00:51 0 model Filter: 
2015-08-12T15:00:52 0 winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o C:\Users\Simon\Documents\EnglishIMD\topo\UKIREPOLY.json --id-property LSOA01CD -p d3Css -s 1e-9 -- l0=C:\Users\Simon\Documents\EnglishIMD\shp\UK_IRE_POLY.shp
2015-08-12T15:00:56 0 winHelper topojson result 
bounds: -10.625570682933017 49.168431613190194 1.7610498126253136 60.86076643797765 (spherical)
pre-quantization: 1.38m (0.0000124Â°) 1.30m (0.0000117Â°)
topology: 3394 arcs, 2037677 points
post-quantization: 138m (0.00124Â°) 130m (0.00117Â°)
simplification: retained 46554 / 391204 points (12%)
prune: retained 868 / 3394 arcs (26%)
2015-08-12T15:00:56 0 model EXPORT LSOA_2001_IMD
2015-08-12T15:00:58 0 model GRADUATED: attr OVRK2010
1 - 3249.1::Most deprived::FILL SYMBOL (1 layers) color 179,0,0,255
3249.1 - 6497.2::||::FILL SYMBOL (1 layers) color 227,74,51,255
6497.2 - 9745.3::|||::FILL SYMBOL (1 layers) color 252,141,89,255
9745.3 - 12993.4::||||::FILL SYMBOL (1 layers) color 253,204,138,255
12993.4 - 16241.5::|||||::FILL SYMBOL (1 layers) color 254,240,217,255
16241.5 - 19489.6::||||||::FILL SYMBOL (1 layers) color 255,255,204,255
19489.6 - 22737.7::|||||||::FILL SYMBOL (1 layers) color 161,218,180,255
22737.7 - 25985.8::||||||||::FILL SYMBOL (1 layers) color 65,182,196,255
25985.8 - 29233.9::|||||||||::FILL SYMBOL (1 layers) color 44,127,184,255
29233.9 - 32482::Least deprived::FILL SYMBOL (1 layers) color 37,52,148,255
2015-08-12T15:00:58 0 model setGraduatedSymbol
2015-08-12T15:00:58 0 model Filter: "OVRK2010" >= 1.0 and "OVRK2010" <= 3249.1
2015-08-12T15:00:59 0 model Filter: "OVRK2010" >= 3249.1 and "OVRK2010" <= 6497.2
2015-08-12T15:01:00 0 model Filter: "OVRK2010" >= 6497.2 and "OVRK2010" <= 9745.3
2015-08-12T15:01:01 0 model Filter: "OVRK2010" >= 9745.3 and "OVRK2010" <= 12993.4
2015-08-12T15:01:02 0 model Filter: "OVRK2010" >= 12993.4 and "OVRK2010" <= 16241.5
2015-08-12T15:01:03 0 model Filter: "OVRK2010" >= 16241.5 and "OVRK2010" <= 19489.6
2015-08-12T15:01:04 0 model Filter: "OVRK2010" >= 19489.6 and "OVRK2010" <= 22737.7
2015-08-12T15:01:05 0 model Filter: "OVRK2010" >= 22737.7 and "OVRK2010" <= 25985.8
2015-08-12T15:01:06 0 model Filter: "OVRK2010" >= 25985.8 and "OVRK2010" <= 29233.9
2015-08-12T15:01:07 0 model Filter: "OVRK2010" >= 29233.9 and "OVRK2010" <= 32482.0
2015-08-12T15:01:10 0 winHelper C:\Program Files\nodejs\node.exe C:\Users\Simon\AppData\Roaming\npm\node_modules\topojson\bin\topojson -o C:\Users\Simon\Documents\EnglishIMD\topo\LSOA2001IMD.json --id-property LSOA01CD -p d3Css -s 1e-9 -- l1=C:\Users\Simon\Documents\EnglishIMD\shp\LSOA_2001_IMD.shp
2015-08-12T15:01:17 0 winHelper topojson result 
bounds: -6.3649789650534805 49.886367784112075 1.762763270374323 55.81105303680311 (spherical)
pre-quantization: 0.904m (0.00000813Â°) 0.659m (0.00000593Â°)
topology: 96721 arcs, 271892 points
post-quantization: 90.4m (0.000813Â°) 65.9m (0.000593Â°)
simplification: retained 269975 / 271792 points (99%)
prune: retained 96720 / 96721 arcs (100%)
2015-08-12T15:01:17 0 bounds Max bounds: -10.6255706829 49.8863677841 1.76276327037 60.860766438
2015-08-12T15:01:17 0 model d3.geo.albers()
     .center([0, 55])
     .rotate([4.0, 0])
     .parallels([49, 61])
     .scale(1000)
     .translate([width / 2, height / 2])
2015-08-12T15:01:21 0 model EXPORT popup data
2015-08-12T15:01:29 0 model EXPORT complete =========================================================```
