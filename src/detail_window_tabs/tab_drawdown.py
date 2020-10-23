#Oggetto rappresentazione di una tab < drawdown >
#Importing a parent file.py
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
#Python libs
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#My Modules
from indexes import *
from tab_obj_canvas import MplCanvas

#Instanciate and manage the drawdown tab, printing drawdown bars
class DrawdownChartTab(QtWidgets.QTabWidget):
    def __init__(self, _trade_list):
        #Calling super <Tab>
        super().__init__()
        #Calculates Local Drawdowns
        dd = Drawdown(_trade_list)
        y_list_of_values = dd.calculate()
        x_list_of_values = [ index for index in range(len(y_list_of_values))]
        sc = MplCanvas(self, width=10, height=6, dpi=75, _yLabel="Drawdown", _xLabel="Index")
        sc.axes.bar(x_list_of_values, y_list_of_values, color='r') #xList, ylist
        sc.setParent(self)