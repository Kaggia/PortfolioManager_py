#graphics.py
#Libreria grafica contenente gli oggetti dell'interfaccia
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from operator import itemgetter
from copy import deepcopy
import os
import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
#My Modules
import CONSTANTS as directory
from os_interactors import FileManager
from trading_system import TradingSystem
from indexes import *
from options import Option
from date import Date
from date import reset_to_monday
from tab_equity import EquityChartTab
from tab_drawdown import DrawdownChartTab
from tab_optimization import OptimizationTab
from tab_options import OptionTab
from tab_report import ReportTab

#Main window where you can manage the whole portfolio
class MainWindow:
    def __init__(self, _portfolio):
        self.current_portfolio = _portfolio
        self.__file_manager__ = FileManager()
        self.__secondary_windows__ = []
        self.isFirstLoad = True
        self.summary = None
        self.isQuantityChangedByMethod = False
        
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
        #Warning wrong quantity label
        self.wrong_qnt_label = QtWidgets.QLabel(self.frame)
        self.wrong_qnt_label.setGeometry(QtCore.QRect(self.spacing_left +460, 400, 175, 31))
        self.font.setPointSize(22)
        self.wrong_qnt_label.setText("Can't load. Quantity is not valid.")
        self.wrong_qnt_label.hide()
    #Load summary of selected TS
    def __load_summary_trading_system__(self):   
        if self.isQuantityChangedByMethod == False:
            ID_instr_to_load = self.remove_selected_item_cbox.currentText()[:self.remove_selected_item_cbox.currentText().find(' :')]
            trade_list = self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].trade_list
            name_index =  self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].__colums_checkList__.index("Label")
            symbol_index = self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].__colums_checkList__.index("Symbol")

            name_text = trade_list[0][name_index]
            symbol_text = trade_list[0][symbol_index]
            qnt_text = str(self.current_portfolio.scalings[int(ID_instr_to_load)-1])

            if self.summary == None:
                font = QtGui.QFont()
                groupBox_ts = QtWidgets.QGroupBox(self.frame)
                groupBox_ts.setGeometry(QtCore.QRect(425, 200, 240, 100))
                gridLayout = QtWidgets.QGridLayout()

                #FIXED_LABELS
                self.summary_text_label_0 = QtWidgets.QLabel(self.frame)
                self.summary_text_label_0.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_text_label_0.setText("")

                self.summary_text_label_1 = QtWidgets.QLabel(self.frame)
                self.summary_text_label_1.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_text_label_1.setText("Summary")

                self.summary_text_label_2 = QtWidgets.QLabel(self.frame)
                self.summary_text_label_2.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_text_label_2.setText("")

                self.summary_name_label = QtWidgets.QLabel(self.frame)
                self.summary_name_label.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_name_label.setText("Name: ")

                self.summary_symbol_label = QtWidgets.QLabel(self.frame)
                self.summary_symbol_label.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_symbol_label.setText("Symbol: ")

                self.summary_qnt_label = QtWidgets.QLabel(self.frame)
                self.summary_qnt_label.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_qnt_label.setText("Quantity: ")
                #VALUE_LABELS
                self.summary_name_value_label = QtWidgets.QLabel(self.frame)
                self.summary_name_value_label.setGeometry(QtCore.QRect(500, 175, 175, 31))
                font.setPointSize(22)
                self.summary_name_value_label.setText(name_text)

                self.summary_symbol_value_label = QtWidgets.QLabel(self.frame)
                self.summary_symbol_value_label.setGeometry(QtCore.QRect(500, 175, 150, 31))
                font.setPointSize(22)
                self.summary_symbol_value_label.setText(symbol_text)

                self.summary_qnt_value_textbox = QtWidgets.QTextEdit(self.frame)
                self.summary_qnt_value_textbox.setGeometry(QtCore.QRect(500, 175, 75, 31))
                font.setPointSize(22)
                self.summary_qnt_value_textbox.setText(qnt_text)

                gridLayout.addWidget(self.summary_text_label_0, 0, 0)
                gridLayout.addWidget(self.summary_text_label_1, 0, 1)
                gridLayout.addWidget(self.summary_text_label_2, 0, 2)
                gridLayout.addWidget(self.summary_name_label, 1, 0)
                gridLayout.addWidget(self.summary_symbol_label, 2, 0)
                gridLayout.addWidget(self.summary_qnt_label, 3, 0)

                gridLayout.addWidget(self.summary_name_value_label, 1, 1)
                gridLayout.addWidget(self.summary_symbol_value_label, 2, 1)
                gridLayout.addWidget(self.summary_qnt_value_textbox, 3, 1)

                groupBox_ts.setLayout(gridLayout)
                groupBox_ts.show()
                self.summary = groupBox_ts

                #Value changed in Textbox in quantity
                self.summary_qnt_value_textbox.textChanged.connect(self.__check_value_of_quantity__)
                self.summary.show()
            else:
                self.summary.show()
                self.summary_name_value_label.setText(name_text)
                self.summary_symbol_value_label.setText(symbol_text)
                self.summary_qnt_value_textbox.setText(qnt_text)
    #Check value of quantity in textbox
    def __check_value_of_quantity__(self):
        ID_instr_to_load = self.remove_selected_item_cbox.currentText()[:self.remove_selected_item_cbox.currentText().find(' :')]
        selected_trading_system = self.current_portfolio.trading_systems[int(ID_instr_to_load)-1]
        market = selected_trading_system.market
        changed_value = self.summary_qnt_value_textbox.toPlainText()

        if market == 'f':
            try:
                float(changed_value)
                self.wrong_qnt_label.hide()
                self.loadDetails_btn.setEnabled(True)
                if float(changed_value) <= 0.0:
                    self.wrong_qnt_label.show()
                    self.loadDetails_btn.setEnabled(False)
                else:
                    #Correct value and update the scaling list
                    self.current_portfolio.update_scaling_by_index(int(ID_instr_to_load)-1, changed_value)
            except ValueError:
                self.wrong_qnt_label.show()
                self.loadDetails_btn.setEnabled(False)
        elif market == 'i':
            try:
                int(changed_value)
                self.wrong_qnt_label.hide()
                self.loadDetails_btn.setEnabled(True)
                if int(changed_value) <= 0:
                    self.wrong_qnt_label.show()
                    self.loadDetails_btn.setEnabled(False)
                else:
                    #Correct value and update the scaling list
                    self.current_portfolio.update_scaling_by_index(int(ID_instr_to_load)-1, changed_value)
            except ValueError:
                self.wrong_qnt_label.show()
                self.loadDetails_btn.setEnabled(False)
        elif market == 'c':
            try:
                float(changed_value)
                int(changed_value)
                self.wrong_qnt_label.hide()
                self.loadDetails_btn.setEnabled(True)
                if float(changed_value) <= 0.0:
                    self.wrong_qnt_label.show()
                    self.loadDetails_btn.setEnabled(False)
                else:
                    #Correct value and update the scaling list
                    self.current_portfolio.update_scaling_by_index(int(ID_instr_to_load)-1, changed_value)
            except ValueError:
                self.wrong_qnt_label.show()
                self.loadDetails_btn.setEnabled(False)      
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
        #Action in combobox
        self.remove_selected_item_cbox.currentTextChanged.connect(self.__load_summary_trading_system__)       
    #ADD_SYSTEM_BUTTON_HANDLER
    def add_system_btn_Onclick(self):
        list_of_files = self.__file_manager__.get_files()
        for selected_file in list_of_files:
            #Add to portfolio
            ts_id = len(self.current_portfolio.trading_systems) + 1
            new_ts = TradingSystem(ts_id, selected_file)
            self.current_portfolio.add_system(new_ts)
            self.current_portfolio.scalings.append(new_ts.volume) #Set the current volume in scaling list
            #add to combobox
            complete_item_name = str(str(new_ts.id) + " : " + str(new_ts.name))
            self.remove_selected_item_cbox.addItem(complete_item_name)
            if (self.loadDetails_selected_item_cbox.currentText() == ""):
                self.loadDetails_selected_item_cbox.addItem("0 : Portfolio")
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)
            else:
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)
        print(self.current_portfolio.scalings)      
    #REMOVE_SYSTEM_BUTTON_HANDLER
    def remove_system_btn_Onclick(self):
        self.isQuantityChangedByMethod = True
        if len(self.current_portfolio.trading_systems)>=1:
            #Removing system from systems combobox
            id_ts_to_remove = self.remove_selected_item_cbox.currentText()[:self.remove_selected_item_cbox.currentText().find(' :')]
            self.current_portfolio.remove_system(int(id_ts_to_remove)-1)
            self.remove_selected_item_cbox.clear()
            self.isQuantityChangedByMethod = False
            #Indexing
            self.current_portfolio.indexing() #re-indexing the ts' with consistent indexes
            
            for ts in self.current_portfolio.trading_systems:
                complete_item_name = str(str(ts.id) + " : " + str(ts.name))
                self.remove_selected_item_cbox.addItem(complete_item_name)
            #Removing system from details combobox
            self.loadDetails_selected_item_cbox.clear()
            self.loadDetails_selected_item_cbox.addItem("0 : Portfolio")
            for ts in self.current_portfolio.trading_systems:
                complete_item_name = str(str(ts.id) + " : " + str(ts.name))
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)
        else:
            print("Clearing")
            self.remove_selected_item_cbox.clear()
        if len(self.current_portfolio.trading_systems)== 0:
            if self.summary != None:
                self.summary.hide()
    #CLEAR_PORTFOLIO_BUTTON_HANDLER
    def clear_portfolio_btn_Onclick(self):
        self.isQuantityChangedByMethod = True
        self.current_portfolio.clear()
        self.remove_selected_item_cbox.clear()
        self.loadDetails_selected_item_cbox.clear()
        if len(self.current_portfolio.trading_systems)== 0:
            if self.summary != None:
                self.summary.hide()
        #reset scalings
        self.current_portfolio.scalings = []
        self.isQuantityChangedByMethod = False
    #close mainwindow
    def close_window_Onclik(self):
        self.frame.close()
    #show detail window of selected ts or portfolio
    def show_details(self):
        if self.isFirstLoad == False:
            print("INFO: This is a second load, last columns of trades will be deleted.")
            for ts in self.current_portfolio.trading_systems:
                for trade in ts.trade_list:
                    if trade[-1] >= 1000000:
                        trade.pop(-1)
        
        net_index = self.current_portfolio.trading_systems[0].__colums_checkList__.index('Net')  
        self.isFirstLoad = False
        ID_instr_to_load = self.loadDetails_selected_item_cbox.currentText()[:self.loadDetails_selected_item_cbox.currentText().find(' :')]
        unordered_list_of_trades = []
        mod_trade = []
        if int(ID_instr_to_load) == 0:
            #Load portfolio details
            print("INFO: Portfolio with ID-> " + str(ID_instr_to_load) + " will be shown in details.")
            for ts in self.current_portfolio.trading_systems:
                for trade in self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].trade_list:
                    for column in trade:
                        if trade.index(column) == net_index:
                            actual_scaling = self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].volume
                            modified_scaling = self.current_portfolio.scalings[ts.id-1]
                            multypling_factor = round(modified_scaling / actual_scaling, 2)
                            value = multypling_factor * trade[net_index]
                            #print("actual-> "+ str(actual_scaling) + " mod_scale-> " + str(modified_scaling) + " value-> " + str(value))
                            mod_trade.append(value)
                        else:
                            mod_trade.append(column)
                    unordered_list_of_trades.append(mod_trade)    
                    mod_trade = []
            self.__secondary_windows__.append(DetailWindow(unordered_list_of_trades))
        else:
            #Load System by ID
            print("INFO: System with ID-> " + str(ID_instr_to_load) + " will be shown in details.")
            for trade in self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].trade_list:
                    for column in trade:
                        mod_trade.append(column)
                    unordered_list_of_trades.append(mod_trade)    
                    mod_trade = []
            actual_scaling = self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].volume
            modified_scaling = self.current_portfolio.scalings[int(ID_instr_to_load)-1]
            multypling_factor = round(modified_scaling / actual_scaling, 2)

            print("Actual scaling: " + str(actual_scaling))
            print("Modified scaling: " + str(modified_scaling))
            print("multypling_factor : " + str(multypling_factor))

            #for trade in unordered_list_of_trades:
            #   trade[net_index] = multypling_factor * trade[net_index]
                
            self.__secondary_windows__.append(DetailWindow(unordered_list_of_trades)) 
#Window where various details are shown
class DetailWindow:
    def __init__(self, _unordered_list_of_trades):
        self.trades_default = deepcopy(_unordered_list_of_trades)
        self.trades = deepcopy(_unordered_list_of_trades)

        self.__order_raw_trade_list__(self.trades_default)
        self.__order_raw_trade_list__(self.trades)

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
        self.tab_options = OptionTab(self.trades, self)
        self.tab_optimization = OptimizationTab()
        self.tabs.resize(720,480)
        # Add tabs
        self.tabs.addTab(self.tab_options,"General options")
        self.tabs.addTab(self.tab_report,"Report")
        self.tabs.addTab(self.tab_drawdown,"Drawdown analysis")
        self.tabs.addTab(self.tab_equity,"Equity analysis")
        self.tabs.addTab(self.tab_optimization,"Optimization")

        #Load Tabs content
        self.__tab_report_loader__()
        self.__tab_equity_loader()
        self.__tab_drawdownChart_loader()
        self.__tab_options_loader()
        self.__tab_optimization_loader()

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
        monthly_return = MonthlyReturn(self.trades)

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
        self.tab_report.add_new_index("Avg monthly return: ", monthly_return.calculate())    
    #load dd tab <NONE>
    def __tab_drawdownChart_loader(self):
        pass
    #load equity tab <NONE>
    def __tab_equity_loader(self):
        pass
    #Load Options tab <NONE>
    def __tab_options_loader(self):
        pass
    #Load Optimization tab
    def __tab_optimization_loader(self):
        pass
    #order tradelist passed
    def __order_raw_trade_list__(self, listoftrades):
        #index_of_date = 0
        #Get the ID of column with dates_format
        for trade in listoftrades:
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
        
        #fm = FileManager()
        #fm.dump_list_of_list("dump.txt", self.trades)      
    #convert a date(string) to a internalDate Value, letting the list be ordered
    def __convert_date_to_internalDate__(self, _month, _day, _year, _hour, _minute):
        day_value = (int(_day) - 1 ) * 1440
        month_value = (int(_month) - 1 ) * 43800
        year_value = (int(_year) - 2000 ) * 524160
        hour_value = int(_hour) * 60
        minute_value = int(_minute)
        sum_of_minutes = day_value + month_value + year_value + hour_value + minute_value

        return sum_of_minutes
    #Get Index of date-column
    def __get_index_of_date_column__(self):
        single_trade = self.trades[0]
        index = -1
        i = 0
        for column in single_trade:
            if len(str(column)) == 16 and (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                index = i
                break
            else:
                i += 1
        return index
    #Filter trades
    def filter_trades_by_option (self, _options):
        new_trades = deepcopy(self.trades)
        trades_to_return = []
        #GetStartingDateAsValue
        starting_date_as_value = self.__convert_date_to_internalDate__(_options.startDate.m, _options.startDate.d, _options.startDate.y, 0, 0)
        #GetEndingDateAsValue
        ending_date_as_value = self.__convert_date_to_internalDate__(_options.endDate.m, _options.endDate.d, _options.endDate.y, 23, 59)
        #Filtering by Start and end date
        index_of_date_column = self.__get_index_of_date_column__()

        for trade in new_trades:
            current_internal_date = self.__convert_date_to_internalDate__(trade[index_of_date_column][0:2], trade[index_of_date_column][3:5], trade[index_of_date_column][6:11], trade[index_of_date_column][11:13], trade[index_of_date_column][14:])
            if (current_internal_date >= starting_date_as_value) and (current_internal_date <= ending_date_as_value) :
                trades_to_return.append(trade)
        #Filtering by time window  
        if _options.time_window == 'D':
            filtered_list_of_trades = []
            for trade in trades_to_return:
                filtered_list_of_trades.append(trade)

        elif _options.time_window == 'd':
            print("Daily filtering options algo")
            list_to_sum = []
            day = []
            DIFF_DAY = self.__convert_date_to_internalDate__(1, 2, 2001, 0, 0) - self.__convert_date_to_internalDate__(1, 1, 2001, 0, 0)
            last_date_of_trade_as_value = self.__convert_date_to_internalDate__(trades_to_return[0][index_of_date_column][0:2], trades_to_return[0][index_of_date_column][3:5], trades_to_return[0][index_of_date_column][6:11], 0, 0)
            print("DIFF_DAY: ", DIFF_DAY)
            for trade in trades_to_return:
                current_date = trade[index_of_date_column]
                current_date_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], current_date[11:13], current_date[14:])
                if (current_date_as_value - last_date_of_trade_as_value) <= DIFF_DAY:
                    print("Differenza tra due trade date<intraday>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    day.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0)
                else:
                    print("Differenza tra due trade date<out of a day>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    list_to_sum.append(day)
                    day = []
                    day.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0)

            #Merging data from the same time interval
            filtered_list_of_trades = []
            index = 0
            name = trades_to_return[0][1]
            symbol = trades_to_return[0][2]
            volume = trades_to_return[0][3]
            closing_date =  None
            net_cumulative = 0
            for day_c in list_to_sum:
                for d in day_c:
                    net_cumulative = net_cumulative + d[-2]
                    closing_date = d[-3][:-6] + " 00:00"
                    name = d[1]
                    symbol = d[2]
                    volume = d[3]
                filtered_list_of_trades.append([index, name, symbol, volume, closing_date, float(net_cumulative), 0])
                net_cumulative = 0
                index += 1

        elif _options.time_window == 'w':
            print("Weekly filtering options algo")
            list_to_sum = []
            week = []
            DIFF_WEEK = (self.__convert_date_to_internalDate__(1, 2, 2001, 0, 0) - self.__convert_date_to_internalDate__(1, 1, 2001, 0, 0)) * 7
            day_tmp = Date(trades_to_return[0][index_of_date_column][3:5], trades_to_return[0][index_of_date_column][0:2], trades_to_return[0][index_of_date_column][6:11])
            #Reset to closer Monday
            last_date_of_trade_as_value = reset_to_monday(day_tmp, self.__convert_date_to_internalDate__(trades_to_return[0][index_of_date_column][0:2], trades_to_return[0][index_of_date_column][3:5], trades_to_return[0][index_of_date_column][6:11], 0, 0))
            
            print("DIFF_WEEK: ", DIFF_WEEK)
            for trade in trades_to_return:
                current_date = trade[index_of_date_column]
                current_date_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], current_date[11:13], current_date[14:])
                if (current_date_as_value - last_date_of_trade_as_value) <= DIFF_WEEK:
                    print("Differenza tra due trade date<intraweek>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    week.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0)
                else:
                    print("Differenza tra due trade date<out of a week>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    list_to_sum.append(week)
                    week = []
                    week.append(trade)
                    day_tmp = Date(current_date[3:5], current_date[0:2], current_date[6:11])
                    #Reset to closer Monday
                    last_date_of_trade_as_value = reset_to_monday(day_tmp, self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], 0, 0))

            #Merging data from the same time interval
            filtered_list_of_trades = []
            index = 0
            name = trades_to_return[0][1]
            symbol = trades_to_return[0][2]
            volume = trades_to_return[0][3]
            closing_date =  None
            net_cumulative = 0
            for week_c in list_to_sum:
                for d in week_c:
                    net_cumulative = net_cumulative + d[-2]
                    closing_date = d[-3][:-6] + " 00:00"
                    name = d[1]
                    symbol = d[2]
                    volume = d[3]
                filtered_list_of_trades.append([index, name, symbol, volume, closing_date, float(net_cumulative), 0])
                net_cumulative = 0
                index += 1

        elif _options.time_window == 'm':
            print("Monthly filtering options algo")
            list_to_sum = []
            month = []
            DIFF_MONTH = self.__convert_date_to_internalDate__(2, 1, 2001, 0, 0) - self.__convert_date_to_internalDate__(1, 1, 2001, 0, 0)
            last_date_of_trade_as_value = self.__convert_date_to_internalDate__(trades_to_return[0][index_of_date_column][0:2], 1, trades_to_return[0][index_of_date_column][6:11], 0, 0)
            print("DIFF_MONTH: ", DIFF_MONTH)
            for trade in trades_to_return:
                current_date = trade[index_of_date_column]
                current_date_as_value = self.__convert_date_to_internalDate__(current_date[0:2], current_date[3:5], current_date[6:11], current_date[11:13], current_date[14:])
                if (current_date_as_value - last_date_of_trade_as_value) <= DIFF_MONTH:
                    print("Differenza tra due trade date<intraday>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    month.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], 1, current_date[6:11], 0, 0)
                else:
                    print("Differenza tra due trade date<out of a day>: ", str(current_date_as_value - last_date_of_trade_as_value))
                    list_to_sum.append(month)
                    month = []
                    month.append(trade)
                    last_date_of_trade_as_value = self.__convert_date_to_internalDate__(current_date[0:2], 1, current_date[6:11], 0, 0)

            #Merging data from the same time interval
            filtered_list_of_trades = []
            index = 0
            name = trades_to_return[0][1]
            symbol = trades_to_return[0][2]
            volume = trades_to_return[0][3]
            closing_date =  None
            net_cumulative = 0
            for month_c in list_to_sum:
                for m in month_c:
                    net_cumulative = net_cumulative + m[-2]
                    closing_date = m[index_of_date_column][0:2] + "/" + m[index_of_date_column][6:-6] + " 00:00"
                    name = m[1]
                    symbol = m[2]
                    volume = m[3]
                filtered_list_of_trades.append([index, name, symbol, volume, closing_date, float(net_cumulative), 0])
                net_cumulative = 0
                index += 1

        #IMPLEMENT
        for trade in filtered_list_of_trades:
            print(trade)

        return filtered_list_of_trades
    #Reloading the tabs 
    def reload_tabs(self, _options):
        #Load trades by options
        filtered_trades_list = self.filter_trades_by_option(_options)
        #for trade in filtered_trades_list:
        #    print(trade)
        #Reload all tabs by removing them and calling them back again
        #<REMOVING>
        self.tabs.removeTab(self.tabs.indexOf(self.tab_options))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_report))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_drawdown))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_optimization))
        self.tabs.removeTab(self.tabs.indexOf(self.tab_equity))
        
        #<ADDING>
        self.tab_report = ReportTab(2, 17, 100, 20) #(index_per_column, spacingX, spacingY)
        self.tab_drawdown = DrawdownChartTab(filtered_trades_list)
        self.tab_equity = EquityChartTab(filtered_trades_list)
        self.tab_options = OptionTab(filtered_trades_list, self)
        self.tab_options.load_state(_options)
        self.tab_optimization = OptimizationTab()

        self.tabs.addTab(self.tab_options,"General options")
        self.tabs.addTab(self.tab_report,"Report")
        self.tabs.addTab(self.tab_drawdown,"Drawdown analysis")
        self.tabs.addTab(self.tab_equity,"Equity analysis")
        self.tabs.addTab(self.tab_optimization,"Optimization")

        #Load Tabs content
        self.__tab_report_loader__()
        self.__tab_equity_loader()
        self.__tab_drawdownChart_loader()
        self.__tab_options_loader()
        self.__tab_optimization_loader()