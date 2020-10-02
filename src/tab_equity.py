#Oggetto rappresentazione di una tab < equity >
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#My Modules
from tab_obj_canvas import MplCanvas

#Instanciate and manage the report tab, printing equity line
class EquityChartTab(QtWidgets.QTabWidget):
    def __init__(self, _trade_list):
        #Calling super <Tab>
        super().__init__()
        #Load x and y axes value
        x_list_of_values = []
        equity_progressive = 0
        y_list_of_values = []
        for trade in _trade_list:
            equity_progressive = equity_progressive + trade[-2]
            x_list_of_values.append(trade[0])
            y_list_of_values.append(equity_progressive)
        sc = MplCanvas(self, width=10, height=6, dpi=75, _yLabel="Equity", _xLabel="Trades")
        sc.axes.plot(x_list_of_values, y_list_of_values) #xList, ylist
        sc.setParent(self)