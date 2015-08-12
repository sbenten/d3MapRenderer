
class chart(object):
    """Base class for a C3 chart object"""
    
    def __init__(self):
        """Constructor"""
        self.name = ""
        self.c3Name = ""
        self.stacked = False
        
    def getStackingScript(self, ranges):
        """Get the javascript for stacking the ranges on top of each other
        
        :param ranges: The names of the data ranges
        :type ranges: list  
              
        :returns: The javascript required for the stacking to work in C3 
        :rtype: string         
        """
        
        # We want a string in the format
        # groups: [['data1', 'data2']]
        
        delimit = """ "data{0}" """
        template = "groups: [[{0}]],"        
        temp = []
        
        if self.stacked == True:  
            i = 1      
            for range in ranges:
                temp.append(delimit.format(i))
                
                i += 1
            
            return template.format(",".join(temp))
        
        else:
            return "" 
        
    def getMinMaxRange(self, main, ranges):
        """Compare the min and max values for all attributes to retrieve the full range of data values

        :param main: The QgsVectorLayer with the data for the viz
        :type main: QgsVectorLayer  
              
        :returns: The min and max values 
        :rtype: int, int 
        """       
        lmin = []
        lmax = []
        
        rmin = 0
        rmax = 0
        
        for r in ranges:
            for f in r.getFields():
                index = main.fieldNameIndex(f)
                lmin.append(main.minimumValue(index))
                lmax.append(main.maximumValue(index))
            
        rmin = min(lmin)   
        if self.stacked == True:
            # stacked charts require the total of the values on the y axis 
           rmax = sum(lmax) 
        else:
            rmax = max(lmax)
            
        return rmin, rmax      
    
    def getJavaScript(self, main, ranges, labels, width, height):
        """Create the chart javascript"""
        
        value = ""
        
        '''Trying to return something along the lines of:
            
         function chart(obj) {
            var par = d3.select(".d3-tip #chart")
            var labels = ["x", 2004, 2007, 2010];
            var data0 = ["data0", obj["OVRK2004"], obj["OVRK2007"], obj["OVRK2010"]];
            var data1 = ["data1", obj["INCRK2004"], obj["INCRK2007"], obj["INCRK2010"]];
    
            var chart = c3.generate({
                bindto: par,
                data: {
                    x: "x",
                    type: "line",
                    columns: [
                      labels,
                      data0,
                      data1
                    ],
                    groups: [
                        ['data0', 'data1']
                    ]
                    names: {
                        data0: "Overall",
                        data1: "Income"
                    }
                },
                size: {
                    width: 240,
                    height: 240
                },
                axis: {
                    y: {
                        min: 0,
                        max: 32000
                    }
                }
            });
        }
        '''
            
        template = """    function chart(obj){{
      var par = d3.select(".d3-tip #chart")
      {labels}
      {vars}
    
      var chart = c3.generate({{
        bindto: par,
        data: {{
          {xaxis}
          type: "{chartName}",
          columns: [
            {labelvar}{data}
          ],
          {groups}
          names: {{ {names} }}
        }},
        size: {{
          width: {width},
          height: {height}
        }},
        axis: {{
          y: {{
            min: {min},
            max: {max}
          }}
        }}
      }});
    }}"""
    
        min, max = self.getMinMaxRange(main, ranges)
        
        # var labels = ["x", 2004, 2007, 2010];
        labelPart = """var labels = ["x", {0}];"""
        labelTemplate = labelPart.format(",".join(labels))
        labelVarTemplate = "labels,"
        
        # var data1 = ["data1", obj["OVRK2004"], obj["OVRK2007"], obj["OVRK2010"]];
        varPart = """var data{0} = ["data{0}", {1}];"""
        fieldPart = """obj["{0}"]"""
        varTemplate = ""
        varList = []
        # Need to check the length of all the labels
        # x: "x",
        xaxisTemplate = """x: "x","""
        for l in labels:
            if len(l) == 0:
                # not all labels specified, so don't need this
                xaxisTemplate = ""
                labelTemplate = ""
                labelVarTemplate = ""
            break
            
        # data1, data2, ...
        dataPart = """data{0}"""
        dataTemplate = ""
        dataList = []
        
        # data1: "Overall", data2: "Income", ...
        namesPart = """data{0}: "{1}" """
        namesTemplate = ""        
        nameList = []
        
        i = 1
        for r in ranges:
            varList.append(varPart.format(str(i), r.getCsvFormattedFields(fieldPart)))
            dataList.append(dataPart.format(str(i)))
            nameList.append(namesPart.format(str(i), r.getName()))     
            
            i += 1
        
        varTemplate = " ".join(varList)
        dataTemplate = ", ".join(dataList)
        namesTemplate = ",".join(nameList)
        
        
        value = template.format(
            labels = labelTemplate,
            vars = varTemplate,
            xaxis = xaxisTemplate,
            chartName = self.c3Name,
            groups = self.getStackingScript(ranges),
            labelvar = labelVarTemplate,
            data = dataTemplate,
            names = namesTemplate,
            width = width,
            height = height,
            min = min,
            max = max
            )

        return value
        
class line(chart):
    """Line chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Line Chart"
        self.c3Name = "line"


class spline(chart):
    """Spline chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Spline Chart"
        self.c3Name = "spline"
        
            
class step(chart):
    """Step chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Step Chart"
        self.c3Name = "step"
        
        
class area(chart):
    """Area chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Area Chart"
        self.c3Name = "area"


class splinearea(chart):
    """Spline area chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Spline Area Chart"
        self.c3Name = "area-spline"
        
class steparea(chart):
    """Stepped area chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Step Area Chart"
        self.c3Name = "area-step"
        
     
class bar(chart):
    """Bar chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Bar Chart"
        self.c3Name = "bar"
        
# TODO: UI needs altering so only one attribute can be selected per range and a 
# warning given to the user if they try and select more than one
class pie(chart):
    """Pie chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Pie Chart"
        self.c3Name = "pie"
        
# TODO: UI needs altering so only one attribute can be selected per range and a 
# warning given to the user if they try and select more than one
class donut(chart):
    """Donut chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Donut Chart"
        self.c3Name = "donut"  
        
class gauge(chart):
    """Gauge chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Gauge Chart"
        self.c3Name = "gauge" 
        
class stackedline(chart):
    """Stacked line chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Line Chart"
        self.c3Name = ""
        self.stacked = True 
        

class stackedspline(chart):
    """Stacked spline chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Spline Chart"
        self.c3Name = "spline"
        self.stacked = True 
                
class stackedstep(chart):
    """Stacked step chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Step Chart"
        self.c3Name = "step"
        self.stacked = True 
 
class stackedarea(chart):
    """Stacked area chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Area Chart"
        self.c3Name = "area"
        self.stacked = True  
        
class stackedsplinearea(chart):
    """Stacked splinee area chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Spline Area Chart"
        self.c3Name = "area-spline"
        self.stacked = True
        
class stackedsteparea(chart):
    """Stacked step area chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Step Area Chart"
        self.c3Name = "area-step"
        self.stacked = True 
        
class stackedbar(chart):
    """Stacked bar chart"""
    
    def __init__(self):
        """Constructor"""
        chart.__init__(self)
        self.name = "Stacked Bar Chart"
        self.c3Name = "bar"
        self.stacked = True 
        
# TODO: Scatterplot requires some UI work to get the X and Y ranges forced on the user
# Would require the user to create ranges in pairs
'''class scatterplot(chart):        
    """Stacked bar chart"""
    
    def __init__(self):
        """Constructor"""
        
        self.name = "Scatterplot"
        self.c3Name = "scatter"'''

       
    
                       

class dataRanges(list):
    """Collection of dataRange objects"""
           
    
    def getRangeCount(self):
        """Retrieve the maximum count of objects within the data ranges"""
        maxLength = 0
        
        for r in self:
            length = r.getLength()
            if length > maxLength:
                maxLength = length
            
        return maxLength
    
    def getQtLabelMask(self):
        """Get the format mask for the data labels""" 
        #Qt input mask. 
        #Require ASCII numeric character followed by 9 optional ASCII numeric characters
        template = "9000000000"
        i = 0
        max = self.getRangeCount()
        temp = []
        
        while i < max:
           temp.append(template)
           i += 1
           
        return ",".join(temp) 
    
class dataRange:
    """Collection of fields to be used in a range of data"""
    
    def __init__(self, name):
        """Create a new data range helper object"""
        self.__name = name
        self.__formattedList = []
        self.__fieldList = []
        
        temp = ""
        if len(name) > 0:
            temp = name + ":"
            temp = temp.ljust(11)            
        
        self.__displayPrompt = temp
    
    def appendField(self, item):
        """Append method to format the field name"""
        self.__formattedList.append(item.ljust(11))
        self.__fieldList.append(item)       
        
    def getName(self):
        """Get the data range name"""
        return self.__name    
        
    def getFields(self):
        """Get the field list in the range"""
        return self.__fieldList
    
    def getCsvFormattedFields(self, formatString):
        """Concatenate the fields together with custom string format"""
        # e.g. obj["{0}"]
        temp = []
        for f in self.__fieldList:
            temp.append(formatString.format(f))
        
        return ",".join(temp)
        
    def getLength(self):  
        """Get the the amount of fields in the data range"""   
        return len(self.__fieldList)         
    
    def getDisplayString(self):
        """Display the list as a whitespace separated string for display in a field
        Each field is limited to 10 characters (shapefile field name length)
        Name displayed at the beginning of the string
        e.g. NAME:      ITEM1      ITEM2      ITEM3      """  
        temp = ""
           
        if len(self.__displayPrompt) > 0:
            temp = self.__displayPrompt
        temp += ', '.join(self.__formattedList)
        
        return temp
        