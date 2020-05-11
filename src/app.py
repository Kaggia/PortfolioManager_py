#graphics.py
#Libreria grafica contenente gli oggetti dell'interfaccia
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from operator import itemgetter
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#My Modules
import CONSTANTS as directory
from os_interactors import FileManager
from trading_system import TradingSystem
from indexes import *

#Main window where you can manage the whole portfolio
class MainWindow:
    def __init__(self, _portfolio):
        self.current_portfolio = _portfolio
        self.__file_manager__ = FileManager()
        self.__secondary_windows__ = []
        self.isFirstLoad = True
        
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(1024, 720)
        self.frame.setWindowTitle("cTrader - Portfolio Manager")
        self.frame.setMinimumSize(QtCore.QSize(720, 480))
        self.frame.setMaximumSize(QtCore.QSize(720, 480))
        self.font = QtGui.QFont()
        self.spacing_left = 25

        fontLogo = QtGui.QFont()
        fontLogo.setPointSize(42)
        self.logoLabel = QtWidgets.QLabel(self.frame)
        self.logoLabel.setFont(fontLogo)
        self.logoLabel.setText("PORTFOLIO MANAGER")
        self.logoLabel.setGeometry(QtCore.QRect(75, 10, 600, 175)) #(posX, posY, dimX, dimY)
        #self.logoLabel.setPixmap(QtGui.QPixmap('logo_small.jpeg'))
        fontLogo_2 = QtGui.QFont()
        fontLogo_2.setPointSize(12)
        self.logoLabel_2 = QtWidgets.QLabel(self.frame)
        self.logoLabel_2.setFont(fontLogo_2)
        self.logoLabel_2.setText("for cTrader")
        self.logoLabel_2.setGeometry(QtCore.QRect(550, 50, 125, 175)) #(posX, posY, dimX, dimY)
        #self.logoLabel.setPixmap(QtGui.QPixmap('logo_small.jpeg'))
        separator_font = QtGui.QFont()
        separator_font.setPointSize(12)
        self.separator = QtWidgets.QLabel(self.frame)
        self.separator.setFont(separator_font)
        self.separator.setText("__________________________________________________________")
        self.separator.setGeometry(QtCore.QRect(90, 275, 800, 175)) #(posX, posY, dimX, dimY)


        self.__load_menu_bar__()
        self.__load_loading_options__()
        self.__add_separator__()
        self.__load_selecting_system__()
        self.__attach_handlers__()
        
        self.frame.show()
    #Load menu bar: File|Options|Help
    def __load_menu_bar__(self):
         #menu
        self.menubar = QtWidgets.QMenuBar(self.frame)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 995, 21))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("File")
        self.menubar.addMenu(self.menuFile)
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setTitle("Options")
        self.menubar.addMenu(self.menuOptions)
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setTitle("Tools")
        self.menubar.addMenu(self.menuTools)
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setTitle("Help")
        self.menubar.addMenu(self.menuHelp)
        self.frame.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.frame)
        self.frame.setStatusBar(self.statusbar)
        #Actions_FILE
        self.actionExitApp = QtWidgets.QAction(self.frame)
        self.actionExitApp.setText("Exit")
        self.menuFile.addAction(self.actionExitApp)
        #Actions_OPTION_add_system
        self.addSystemOption = QtWidgets.QAction(self.frame)
        self.addSystemOption.setText("Add system(s)")
        self.menuOptions.addAction(self.addSystemOption)
        #Actions_OPTION_clear_pf
        self.clearPortfolio = QtWidgets.QAction(self.frame)
        self.clearPortfolio.setText("Clear Portfolio")
        self.menuOptions.addAction(self.clearPortfolio)
    #Load the section relative to loading options
    def __load_loading_options__(self):
        #Label_loading_opt
        y = 175
        self.load_option_label = QtWidgets.QLabel(self.frame)
        self.load_option_label.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.load_option_label.setText("Load options:")

        #Button_ADD_SYSTEM
        y += 35
        self.add_system_btn = QtWidgets.QPushButton(self.frame)
        self.add_system_btn.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.add_system_btn.setText("Add system(s)")
        #Button_REMOVE_SYSTEM
        y += 35
        self.remove_system_btn = QtWidgets.QPushButton(self.frame)
        self.remove_system_btn.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.remove_system_btn.setText("Remove selected system")
        #Combobox_REMOVE_SELECTED_ITEM
        self.remove_selected_item_cbox = QtWidgets.QComboBox(self.frame)
        self.remove_selected_item_cbox.setGeometry(QtCore.QRect(self.spacing_left + 150, y, 150, 31))
        #Button_CLEAR_PORTFOLIO
        y += 35
        self.clear_portfolio_btn = QtWidgets.QPushButton(self.frame)
        self.clear_portfolio_btn.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.clear_portfolio_btn.setText("Clear Portfolio")
    #Define a separator, based on png file
    def __add_separator__(self):
       pass
    #Load the sectione relative to the selection of a single or multiple systems
    def __load_selecting_system__(self):
        #LABEL
        self.load_system_label = QtWidgets.QLabel(self.frame)
        self.load_system_label.setGeometry(QtCore.QRect(self.spacing_left, 400, 150, 31))
        self.font.setPointSize(22)
        self.load_system_label.setText("Load system or Portfolio:")
        #SELECT_SYSTEM_CBOX
        self.loadDetails_selected_item_cbox = QtWidgets.QComboBox(self.frame)
        self.loadDetails_selected_item_cbox.setGeometry(QtCore.QRect(self.spacing_left + 150, 400, 150, 31))
        #Button_LOAD_DETAILS
        self.loadDetails_btn = QtWidgets.QPushButton(self.frame)
        self.loadDetails_btn.setGeometry(QtCore.QRect(self.spacing_left +300, 400, 150, 31))
        self.font.setPointSize(22)
        self.loadDetails_btn.setText("Load details")
    #Attach event handlers to the graphical obj
    def __attach_handlers__(self):
        self.add_system_btn.clicked.connect(self.add_system_btn_Onclick)
        self.remove_system_btn.clicked.connect(self.remove_system_btn_Onclick)
        self.clear_portfolio_btn.clicked.connect(self.clear_portfolio_btn_Onclick)
        self.loadDetails_btn.clicked.connect(self.show_details)
        #Action in menus
        self.actionExitApp.triggered.connect(self.close_window_Onclik)
        self.addSystemOption.triggered.connect(self.add_system_btn_Onclick)
        self.clearPortfolio.triggered.connect(self.clear_portfolio_btn_Onclick)
    #ADD_SYSTEM_BUTTON_HANDLER
    def add_system_btn_Onclick(self):
        list_of_files = self.__file_manager__.get_files()
        for selected_file in list_of_files:
            #Add to portfolio
            ts_id = len(self.current_portfolio.trading_systems) + 1
            new_ts = TradingSystem(ts_id, selected_file)
            self.current_portfolio.add_system(new_ts)
            #add to combobox
            complete_item_name = str(str(new_ts.id) + " : " + str(new_ts.name))
            self.remove_selected_item_cbox.addItem(complete_item_name)
            if (self.loadDetails_selected_item_cbox.currentText() == ""):
                self.loadDetails_selected_item_cbox.addItem("0 : Portfolio")
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)
            else:
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)
    #REMOVE_SYSTEM_BUTTON_HANDLER
    def remove_system_btn_Onclick(self):
        if len(self.current_portfolio.trading_systems)>1:
            id_ts_to_remove = self.remove_selected_item_cbox.currentText()[:self.remove_selected_item_cbox.currentText().find(' :')]
            self.current_portfolio.remove_system(int(id_ts_to_remove)-1)
            self.remove_selected_item_cbox.clear()
            for ts in self.current_portfolio.trading_systems:
                complete_item_name = str(str(ts.id) + " : " + str(ts.name))
                self.remove_selected_item_cbox.addItem(complete_item_name)
        else:
            self.remove_selected_item_cbox.clear()
    #CLEAR_PORTFOLIO_BUTTON_HANDLER
    def clear_portfolio_btn_Onclick(self):
        self.current_portfolio.clear()
        self.remove_selected_item_cbox.clear()
        self.loadDetails_selected_item_cbox.clear()
    #close mainwindow
    def close_window_Onclik(self):
        self.frame.close()
    #show detail window of selected ts or portfolio
    def show_details(self):
        if self.isFirstLoad == False:
            print("INFO: This is a second load, last columns of trades will be deleted.")
            for ts in self.current_portfolio.trading_systems:
                for trade in ts.trade_list:
                    trade.pop(-1)
            
        self.isFirstLoad = False
        ID_instr_to_load = self.loadDetails_selected_item_cbox.currentText()[:self.loadDetails_selected_item_cbox.currentText().find(' :')]
        unordered_list_of_trades = []
        if int(ID_instr_to_load) == 0:
            #Load portfolio details
            print("INFO: Portfolio with ID-> " + str(ID_instr_to_load) + " will be shown in details.")
            for ts in self.current_portfolio.trading_systems:
                for trade in ts.trade_list:
                    unordered_list_of_trades.append(trade)

                
            self.__secondary_windows__.append(DetailWindow(unordered_list_of_trades))
        else:
            #Load System by ID
            print("INFO: System with ID-> " + str(ID_instr_to_load) + " will be shown in details.")
            for trade in self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].trade_list:
                    unordered_list_of_trades.append(trade)
                
            self.__secondary_windows__.append(DetailWindow(unordered_list_of_trades)) 
#Window where various details are shown
class DetailWindow:
    def __init__(self, _unordered_list_of_trades, _timeFilter='01/01/2000 00:00'):
        self.trades = _unordered_list_of_trades
        self.__order_raw_trade_list__()
        self.trades = self.__select_data_from__(_timeFilter)
        for trade in self.trades:
            print(trade)
        
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(720, 480)
        self.frame.setWindowTitle("cTrader - Portfolio Manager - Detail window")
        self.frame.setMinimumSize(QtCore.QSize(720, 480))
        self.frame.setMaximumSize(QtCore.QSize(720, 480))
        self.font = QtGui.QFont()
        
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget(self.frame)
        self.tab_report = ReportTab(2, 17, 100, 20) #(index_per_column, spacingX, spacingY)
        self.tab_drawdown = DrawdownChartTab(self.trades)
        self.tab_equity = EquityChartTab(self.trades)
        self.tabs.resize(720,480)
        # Add tabs
        self.tabs.addTab(self.tab_report,"Tab Report")
        self.tabs.addTab(self.tab_drawdown,"Tab Drawdown")
        self.tabs.addTab(self.tab_equity,"Tab Equity")
        #Load Tabs content
        self.__tab_report_loader__()
        self.__tab_equity_loader()
        self.__tab_drawdownChart_loader()

        self.frame.show()
    #load report tab
    def __tab_report_loader__(self):
        _ = CustomIndex(self.trades)
        _ = Symbol(self.trades)
        name_of_ts = Name(self.trades)
        symbol_of_ts = FormattedSymbol(self.trades)
        equity = Equity(self.trades)
        max_dd = MaximumDrawdown(self.trades)
        gross_profit = GrossProfit(self.trades)
        gross_loss = GrossLoss(self.trades)
        profit_factor = ProfitFactor(self.trades)
        total_trades = TotalNumberOfTrades(self.trades)
        winning_trades = WinningTrades(self.trades)
        losing_trades = LosingTrades(self.trades)
        percent_profitable = PercentProfitable(self.trades)
        even_trades = EvenTrades(self.trades)
        avg_trade_net_profit = AvgTradeNetProfit(self.trades)
        avg_winning_trade = AvgWinningTrade(self.trades)
        avg_losing_trade = AvgLosingTrade(self.trades)
        largest_win_trade = LargestWinningTrade(self.trades)
        largest_los_trade = LargestLosingTrade(self.trades)
        max_win_streak = MaxWinningStreak(self.trades)
        max_los_streak = MaxLosingStreak(self.trades)
        size_require = SizeRequirement(self.trades)

        self.tab_report.add_text(name_of_ts.calculate() + symbol_of_ts.calculate())
        self.tab_report.add_new_index("Net Profit: ", equity.calculate())
        self.tab_report.add_new_index("Drawdown(max): ", max_dd.calculate())
        self.tab_report.add_new_index("Gross Profit: ", gross_profit.calculate())
        self.tab_report.add_new_index("Gross Loss: ", gross_loss.calculate())
        self.tab_report.add_new_index("Profit Factor: ", profit_factor.calculate())
        self.tab_report.add_text("")
        self.tab_report.add_text("Trades info")
        self.tab_report.add_new_index("Total trades: ", total_trades.calculate())
        self.tab_report.add_new_index("Winning trades: ", winning_trades.calculate())
        self.tab_report.add_new_index("Losing trades: ", losing_trades.calculate())
        self.tab_report.add_new_index("Percent profitable: ", str(percent_profitable.calculate()) + " %")
        self.tab_report.add_new_index("Even trades: ", even_trades.calculate())
        self.tab_report.add_new_index("Avg profit per trade: ", avg_trade_net_profit.calculate())
        self.tab_report.add_new_index("Avg Winning trade: ", avg_winning_trade.calculate())
        self.tab_report.add_new_index("Avg Losing trade: ", avg_losing_trade.calculate())
        self.tab_report.add_new_index("Largest winning: ", largest_win_trade.calculate())
        self.tab_report.add_new_index("Largest losing: ", largest_los_trade.calculate())
        self.tab_report.add_text("")
        self.tab_report.add_new_index("Max Win streak: ", max_win_streak.calculate())
        self.tab_report.add_new_index("Max Lose streak: ", max_los_streak.calculate())
        self.tab_report.add_new_index("Size required: ", size_require.calculate())
    #load dd tab
    def __tab_drawdownChart_loader(self):
        pass
    #load equity tab
    def __tab_equity_loader(self):
        pass
    #order tradelist passed
    def __order_raw_trade_list__(self):
        #index_of_date = 0
        #Get the ID of column with dates_format
        for trade in self.trades:
            for column in trade:
                if len(str(column)) == 16:
                    if (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                        #Column found is a valid date 
                        internal_date = self.__convert_date_to_internalDate__(column[0:2], column[3:5], column[6:11], column[11:13], column[14:])
                        trade.append(internal_date)
                        break  
                
        #For every trade add a column with value, derived from date format
        ordered_list = sorted(self.trades, key=itemgetter(-1))
        self.trades = ordered_list
        #re-assign progressive ids
        trade_id = 0
        for trade in self.trades:
            trade[0] = trade_id
            trade_id += 1
    #selects data from the date specifiend on
    def __select_data_from__(self, _timeFilter):
        internal_date = self.__convert_date_to_internalDate__(_timeFilter[0:2], _timeFilter[3:5], _timeFilter[6:11], _timeFilter[11:13], _timeFilter[14:])
        selected_trades_to_show = []
        for trade in self.trades:
            if trade[-1] >= internal_date:
                selected_trades_to_show.append(trade)

        return selected_trades_to_show
    
    #convert a date(string) to a internalDate Value, letting the list be ordered
    def __convert_date_to_internalDate__(self, _day, _month, _year, _hour, _minute):
        day_value = (int(_day) - 1 ) * 1440
        month_value = (int(_month) - 1 ) * 43800
        year_value = (int(_year) - 2000 ) * 524160
        hour_value = int(_hour) * 60
        minute_value = int(_minute)
        sum_of_minutes = day_value + month_value + year_value + hour_value + minute_value

        return sum_of_minutes
#Instanciate and manage the report tab, printing all indexes
class ReportTab(QtWidgets.QTabWidget):
    def __init__(self,_columns, _rows, _spacingX, _spacingY):
        #Calling super <Tab>
        super().__init__()
        #<self> variable refers to the <Tab>
        self.rows = _rows  
        self.grid_counting = {"X": 0, "Y": 0}
        self.column_distancing = self.width() / (_columns * 2)
        self.positioning_cursor = {"X": 10, "Y": -20} #Posizione del cursore per il posizionamento
        self.spacing = {"X": _spacingX, "Y": _spacingY} #Spazio tra gli elementi
    #add a new index specifying <index_name> and his <value>
    def add_new_index(self, _index_name, _index_value):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        index_text_label = QtWidgets.QLabel(self)
        index_text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_text_label.setText(_index_name)
        #index_value
        index_value_label = QtWidgets.QLabel(self)
        index_value_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + self.spacing["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_value_label.setText(str(_index_value))
        self.__grid_counting__()
    #add a simple text
    def add_text(self, _text_to_show):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        text_label = QtWidgets.QLabel(self)
        text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        text_label.setText(_text_to_show)
        self.__grid_counting__()
    #when you add a row, manage the colums
    def __grid_counting__(self):
        self.grid_counting["X"] += 1
        if self.grid_counting["X"] > self.rows :
            #si è superato il limite di righe
            self.grid_counting["X"] = 0
            self.grid_counting["Y"] += 1
            #Reset cursor for Y
            self.positioning_cursor["Y"] = -20
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
#Canvas class to manage a chart
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, _yLabel="", _xLabel=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_ylabel(_yLabel)
        self.axes.set_xlabel(_xLabel)
        super(MplCanvas, self).__init__(fig)

 