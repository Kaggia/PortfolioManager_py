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
#MyLibs
from trading_system import TradingSystemSchema
from date import CompleteDate
from indexes import Equity

class TemporalAnalysisWindow:
    def __init__(self, _trade_list):
        self.trade_list = deepcopy(_trade_list)
        self.trade_list_default = deepcopy(_trade_list)
        self.book = [] #Chart data
        self.current_page_shown = 0

        
        self.__gui_load__()
        self.__detect_initial_temporal_view__()
        self.load_data_as_book(bar_per_page = 4)
        #Set next button state
        if len(self.book) == 1:
            self.next_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(True)


        self.frame.show()
        #Setting the chart inside the canvas obj
        self.canvas_chart = MplCanvas(self.frame, width=12, height=4, dpi=70, _yLabel="Y", _xLabel="X")
        self.load_data_on_chart(self.book, 0)

    #Load GUI elements
    def __gui_load__(self):
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(840, 560)
        self.frame.setWindowTitle("cTrader - Portfolio Manager - Temporal Analysis")
        self.frame.setMinimumSize(QtCore.QSize(840, 560))
        self.frame.setMaximumSize(QtCore.QSize(840, 560))

        #Button_Previous
        self.prev_btn = QtWidgets.QPushButton(self.frame)
        self.prev_btn.setGeometry(QtCore.QRect((self.frame.size().width() / 2) - 100, int(self.frame.size().height() *0.57), 100, 40))
        self.prev_btn.setText("<= Previous page")
        self.prev_btn.setEnabled(False)
        #Button_Previous
        self.next_btn = QtWidgets.QPushButton(self.frame)
        self.next_btn.setGeometry(QtCore.QRect((self.frame.size().width() / 2), int(self.frame.size().height() *0.57), 100, 40))
        self.next_btn.setText("Next page =>")
        
        
        #Groupbox_loaders
        self.__load_groupbox_temp_selection__()
        self.__load_groupbox_year_selection__()
        self.__load_groupbox_month_selection__()

        #handlers
        self.yearly_choice_rb.clicked.connect(self.yearly_choice_rb_onClick)
        self.monthly_choice_rb.clicked.connect(self.monthly_choice_rb_onClick)
        self.prev_btn.clicked.connect(self.prev_btn_onClick)
        self.next_btn.clicked.connect(self.next_btn_onClick)

        #Set the initial groupbox state
        self.yearly_choice_rb_onClick()
    def __load_groupbox_temp_selection__(self):
        self.groupbox_temp_choice = QtWidgets.QGroupBox("Choose temporal window", self.frame )
        self.groupbox_temp_choice.setGeometry(QtCore.QRect(50, 450, 175, 100))
        
        vbox = QtWidgets.QVBoxLayout()
        self.groupbox_temp_choice.setLayout(vbox)

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
        self.groupbox_year_choice = QtWidgets.QGroupBox("Choose year to show", self.frame )
        self.groupbox_year_choice.setGeometry(QtCore.QRect(250, 450, 175, 100))
        
        vbox = QtWidgets.QVBoxLayout()
        self.groupbox_year_choice.setLayout(vbox)

        #Combobox
        self.combobox_year_select = QtWidgets.QComboBox()
        self.combobox_year_select.setGeometry(QtCore.QRect(300, 450 , 150, 25))
        self.combobox_year_select.addItem('2000')
        self.combobox_year_select.addItem('2001')
        self.combobox_year_select.addItem('2002')

        self.combobox_year_select.setCurrentIndex(0)

        vbox.addWidget(self.combobox_year_select)

    def __load_groupbox_month_selection__(self):
        self.groupbox_month_choice = QtWidgets.QGroupBox("Choose month to show", self.frame )
        self.groupbox_month_choice.setGeometry(QtCore.QRect(450, 450, 175, 100))
        
        vbox = QtWidgets.QVBoxLayout()
        self.groupbox_month_choice.setLayout(vbox)

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
    #Previous button handler method
    def prev_btn_onClick(self):
        print("Button Previous pressed.")
        self.current_page_shown -=1
        #SHOW ON CHART
        #Check page
        if self.current_page_shown == 0:
            self.prev_btn.setEnabled(False)
        else:
            self.prev_btn.setEnabled(True)
        if self.current_page_shown == len(self.book)-1:
            self.next_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(True)
        self.load_data_on_chart(self.book, self.current_page_shown)
    #Next button handler method    
    def next_btn_onClick(self):
        print("Button Next pressed.")
        self.current_page_shown +=1
        #SHOW ON CHART
        #Check start of book
        if self.current_page_shown == 0:
            self.prev_btn.setEnabled(False)
        else:
            self.prev_btn.setEnabled(True)
        #Check end of book
        if self.current_page_shown == len(self.book)-1:
            self.next_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(True)  
        self.load_data_on_chart(self.book, self.current_page_shown)
    #Radiobutton Handlers
    def monthly_choice_rb_onClick(self):
        self.groupbox_month_choice.setVisible(False)
        self.groupbox_year_choice.setVisible(True)
    def yearly_choice_rb_onClick(self):
        self.groupbox_year_choice.setVisible(False)
        self.groupbox_month_choice.setVisible(False)    
    #Detect temporal view: YEARS - MONTHS - DAYS
    def __detect_initial_temporal_view__(self):
        tss = TradingSystemSchema()
        date_index = tss.date_index_column
        first_date = CompleteDate(self.trade_list[0][date_index][0:2],
                                    self.trade_list[0][date_index][3:5],
                                      self.trade_list[0][date_index][6:11],
                                        self.trade_list[0][date_index][11:13],
                                          self.trade_list[0][date_index][14:])
        last_date = CompleteDate(self.trade_list[-1][date_index][0:2],
                                    self.trade_list[-1][date_index][3:5],
                                      self.trade_list[-1][date_index][6:11],
                                        self.trade_list[-1][date_index][11:13],
                                          self.trade_list[-1][date_index][14:])
        print("First date of trade-> ", first_date.internal_date)
        print("Last date of trade-> ", last_date.internal_date)

        YEAR_ANALSYSIS_SOIL = 525600

        date_diff = last_date.internal_date - first_date.internal_date

        if date_diff > YEAR_ANALSYSIS_SOIL:
            self.yearly_choice_rb_onClick()
            print("[INFO] Temporal window automatically chosen is: Yearly")
        else:
            self.monthly_choice_rb_onClick()
            print("[INFO] Temporal window automatically chosen is: Monthly")
    #Filter trade list to adapt to trade view
    def __filter_data_by_temporal_view(self, _tv):
        pass
    #Load data on chart as book, collection of pages->collection of TradesByYear->Collection of trades
    def load_data_as_book(self, bar_per_page):
        trades = deepcopy(self.trade_list)
        tss = TradingSystemSchema()
        self.book = []
        
        if self.monthly_choice_rb.isChecked():
            print("Start Monthly filtering")
        elif self.yearly_choice_rb.isChecked():
            print("Start Yearly filtering")
            first_date_resetted = CompleteDate(1,
                            1,
                              trades[0][tss.date_index_column][6:11],
                                0,
                                    0)
            last_date_resetted = CompleteDate(1,
                            1,
                                trades[-1][tss.date_index_column][6:11],
                                0,
                                    0)
            year_counter = last_date_resetted.internal_date
            YEAR_IN_MINS = 525600
            list_of_trade_by_years = []
            #Create a list of years <empty>
            for y in range(first_date_resetted.y, last_date_resetted.y + 1):
                list_of_trade_by_years.append(TradesByYear(y))
            #Fill a list of years <empty>
            for trade in trades:
                current_date = CompleteDate(trade[tss.date_index_column][0:2],
                                                trade[tss.date_index_column][3:5],
                                                    trade[tss.date_index_column][6:11],
                                                        0,
                                                            0)
                current_year = current_date.y
                #inserire il trade nella lista dell'anno <current_year>
                list_of_trade_by_years[int(current_year-first_date_resetted.y)].add_trade(trade)
            #Print data on chart as a book
            
            i = 0
            page = []
            for year_of_trades in list_of_trade_by_years:
                if i < 3 :
                    page.append(year_of_trades)
                    i +=1
                else:
                    i = 0
                    self.book.append(page)
                    page = []
                    page.append(year_of_trades)
                    i +=1

    def load_data_on_chart(self, book, index_page_to_show):
        #la pagina contiene i dati
        page_to_show = book[index_page_to_show]
        x_list = []
        y_list = []
        colors = []
        for tby in page_to_show:
            y_list.append(tby.getEquity())
            x_list.append(tby.year)
            if(tby.getEquity() > 0):
                colors.append('g') 
            else:
                colors.append('r')
        
        self.canvas_chart = MplCanvas(self.frame, width=12, height=4, dpi=70, _yLabel="Y", _xLabel="X")
        self.canvas_chart.axes.bar(x_list, y_list, align='center', color=colors, width=0.25) #xList, ylist, align, list_of_colors
        self.canvas_chart.setParent(self.frame)
        self.canvas_chart.show()
class TradesByYear:
    def __init__(self,_year):
        self.year = _year
        self.trade_list = []
    #Add single trade to the year of trade
    def add_trade(self, _trade):
        trade = deepcopy(_trade)
        self.trade_list.append(trade)
    #Return the equity of this year
    def getEquity(self):
        equity = Equity(self.trade_list)
        if not self.trade_list:
            return 0
        else:
            return equity.calculate()
    #Print some data
    def print_data(self):
        print("Year: ", self.year)
        for trade in self.trade_list:
            print(trade)
        print("Equity of this year-> ", str(self.getEquity()))
        print("------------------")