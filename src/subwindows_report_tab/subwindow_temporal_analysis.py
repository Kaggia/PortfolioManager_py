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
        self.prev_btn.setGeometry(QtCore.QRect((self.frame.size().width() / 2) - 100, int(self.frame.size().height() *0.70), 100, 40))
        self.prev_btn.setText("<= Previous page")
        self.prev_btn.setEnabled(True)
        #Button_Previous
        self.next_btn = QtWidgets.QPushButton(self.frame)
        self.next_btn.setGeometry(QtCore.QRect((self.frame.size().width() / 2), int(self.frame.size().height() *0.70), 100, 40))
        self.next_btn.setText("Next page =>")
        self.next_btn.setEnabled(True)

        self.__load_groupbox_temp_selection__()
        self.__load_groupbox_year_selection__()
        self.__load_groupbox_month_selection__()


    def __load_groupbox_temp_selection__(self):
        groupbox_temp_choice = QtWidgets.QGroupBox("Choose temporal window", self.frame )
        groupbox_temp_choice.setGeometry(QtCore.QRect(50, 450, 175, 100))
        
        vbox = QtWidgets.QVBoxLayout()
        groupbox_temp_choice.setLayout(vbox)

        #RadioButton
        self.monthly_choice_rb = QtWidgets.QRadioButton()
        self.monthly_choice_rb.setGeometry(QtCore.QRect(100, 450, 100, 40))
        self.monthly_choice_rb.setText("Monthly")
        self.monthly_choice_rb.setEnabled(True)
        self.monthly_choice_rb.setChecked(False)

        #RadioButton
        self.yearly_choice_rb = QtWidgets.QRadioButton()
        self.yearly_choice_rb.setGeometry(QtCore.QRect(100, 475, 100, 40))
        self.yearly_choice_rb.setText("Yearly")
        self.yearly_choice_rb.setEnabled(True)
        self.yearly_choice_rb.setChecked(True)

        vbox.addWidget(self.monthly_choice_rb)
        vbox.addWidget(self.yearly_choice_rb)

    def __load_groupbox_year_selection__(self):
        groupbox_year_choice = QtWidgets.QGroupBox("Choose year to show", self.frame )
        groupbox_year_choice.setGeometry(QtCore.QRect(250, 450, 175, 100))
        
        vbox = QtWidgets.QVBoxLayout()
        groupbox_year_choice.setLayout(vbox)

        #Combobox
        self.combobox_year_select = QtWidgets.QComboBox()
        self.combobox_year_select.setGeometry(QtCore.QRect(300, 450 , 150, 25))
        self.combobox_year_select.addItem('2000')
        self.combobox_year_select.addItem('2001')
        self.combobox_year_select.addItem('2002')

        self.combobox_year_select.setCurrentIndex(0)

        vbox.addWidget(self.combobox_year_select)

    def __load_groupbox_month_selection__(self):
        groupbox_month_choice = QtWidgets.QGroupBox("Choose month to show", self.frame )
        groupbox_month_choice.setGeometry(QtCore.QRect(450, 450, 175, 100))
        
        vbox = QtWidgets.QVBoxLayout()
        groupbox_month_choice.setLayout(vbox)

        #Combobox
        self.combobox_month_select = QtWidgets.QComboBox()
        self.combobox_month_select.setGeometry(QtCore.QRect(500, 450 , 150, 25))
        self.combobox_month_select.addItem('January')
        self.combobox_month_select.addItem('February')
        self.combobox_month_select.addItem('March')
        self.combobox_month_select.addItem('April')
        self.combobox_month_select.addItem('May')
        self.combobox_month_select.addItem('June')
        self.combobox_month_select.addItem('July')
        self.combobox_month_select.addItem('August')
        self.combobox_month_select.addItem('September')
        self.combobox_month_select.addItem('October')
        self.combobox_month_select.addItem('November')
        self.combobox_month_select.addItem('December')

        self.combobox_month_select.setCurrentIndex(0)

        vbox.addWidget(self.combobox_month_select)
    #Detect temporal view: YEARS - MONTHS - DAYS
    def __detect_initial_temporal_view__(self):
        temporal_view = 'd'

        return temporal_view
    #Filter trade list to adapt to trade view
    def __filter_data_by_temporal_view(self, _tv):
        pass
    #Load data on chart
    def load_data_on_chart(self):
        if self.current_temporal_view == 'm':
            pass
        elif self.current_temporal_view == 'y':
            pass

