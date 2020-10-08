#Frame shows Profit and DD with a temporal frame

#Importing a parent file.py
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from tab_obj_canvas import MplCanvas
from PyQt5 import QtCore, QtGui, QtWidgets

class TemporalAnalysisWindow:
    def __init__(self, _trade_list):
        self.trade_list = deepcopy(_trade_list)
        self.trade_list_default = deepcopy(_trade_list)
        self.current_temporal_view = self.__detect_initial_temporal_view__()

        self.__gui_load__()


        self.frame.show()
        #Setting the chart inside the canvas obj
        sc = MplCanvas(self.frame, width=12, height=4, dpi=70, _yLabel="Y", _xLabel="X")
        sc.axes.hist([0, 1, 2]) #xList, ylist
        sc.setParent(self.frame)
        sc.show()
        print("Temporal analysis window is fully loaded.")
    #Load GUI elements
    def __gui_load__(self):
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(840, 560)
        self.frame.setWindowTitle("cTrader - Portfolio Manager - Temporal Analysis")
        self.frame.setMinimumSize(QtCore.QSize(840, 560))
        self.frame.setMaximumSize(QtCore.QSize(840, 560))

        #Button_Previous
        self.prev_btn = QtWidgets.QPushButton(self.frame)
        self.prev_btn.setGeometry(QtCore.QRect((self.frame.size().width() / 2) - 100, int(self.frame.size().height() *0.6), 100, 40))
        self.prev_btn.setText("<= Previous page")
        self.prev_btn.setEnabled(True)
        #Button_Previous
        self.next_btn = QtWidgets.QPushButton(self.frame)
        self.next_btn.setGeometry(QtCore.QRect((self.frame.size().width() / 2), int(self.frame.size().height() *0.6), 100, 40))
        self.next_btn.setText("Next page =>")
        self.next_btn.setEnabled(True)

    #Detect temporal view: YEARS - MONTHS - DAYS
    def __detect_initial_temporal_view__(self):
        temporal_view = 'd'

        return temporal_view
    #Filter trade list to adapt to trade view
    def __filter_data_by_temporal_view(self, _tv):
        pass
    #Load data on chart
    def load_data_on_chart(self):
        if self.current_temporal_view == 'd':
            pass
        elif self.current_temporal_view == 'm':
            pass
        elif self.current_temporal_view == 'y':
            pass

