#Oggetto rappresentazione di una tab < Optmization >
from PyQt5 import QtCore, QtGui, QtWidgets

#Instanciate and manage the Optimization tab
class OptimizationTab(QtWidgets.QTabWidget):
    def __init__(self):
        #Calling super <Tab>
        super().__init__()