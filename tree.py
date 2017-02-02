import os

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QTreeWidgetItem, QIcon

from layer import vector

class vectorItem(QTreeWidgetItem):
    """User interface item. Wrapper for vector layers to be added to a QTreeWidget"""
    
    layerIcon = QIcon(os.path.join(os.path.dirname(__file__), "img", "layer.png"))
    
    def __init__(self, vector):
        """A new QTreeWidgetItem with the QGis layer information added.

        :param isVisible: Is the layer visible within the legend.
        :type isVisible: bool

        :param vector: Vector object from the mapModel
        :type vector: model.vector"""
        
        QTreeWidgetItem.__init__(self)
        self.setText(0, vector.name)
        self.setIcon(0, self.layerIcon)
        if vector.isVisible:
            self.setCheckState(0, Qt.Checked)
        else:
            self.setCheckState(0, Qt.Unchecked)
            
class fieldItem(QTreeWidgetItem):
    """User interface item. Wrapper for layer fields to be added to a QTreeWidget"""
    
    fieldIcon = QIcon(os.path.join(os.path.dirname(__file__), "img", "field.png"))
    
    def __init__(self, name):
        """A new QTreeWidgetItem with the QGis layer information added.

        :param name: The name of the field in the attribute table
        :type name: string"""
        
        QTreeWidgetItem.__init__(self)
        self.setText(0, name)
        self.setIcon(0, self.fieldIcon)
        self.setCheckState(0, Qt.Unchecked)