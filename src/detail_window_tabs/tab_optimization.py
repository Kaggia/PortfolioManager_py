#Oggetto rappresentazione di una tab < Optmization >
#Importing a parent file.py
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
#Python libs
from PyQt5 import QtCore, QtGui, QtWidgets

#Instanciate and manage the Optimization tab
class OptimizationTab(QtWidgets.QTabWidget):
    def __init__(self):
        #Calling super <Tab>
        super().__init__()