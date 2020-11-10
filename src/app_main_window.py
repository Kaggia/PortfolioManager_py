#app_main_window.py
#Libreria contenente la finestra principale, loading dei trading systems
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from operator import itemgetter
from copy import deepcopy
import random
import os
import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
#My Modules
import CONSTANTS as directory
from os_interactors import FileManager
from trading_system import TradingSystem, TradingSystemSchema
from indexes import *
from options import Option
from date import Date
from date import reset_to_monday
from app_detail_window import DetailWindow
from app_help_window import HelpWindow

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
        #Action Help frame
        self.openHelpFrame = QtWidgets.QAction(self.frame)
        self.openHelpFrame.setText("About")
        self.menuHelp.addAction(self.openHelpFrame)
    #Load the section relative to loading options
    def __load_loading_options__(self):
        #Label_loading_opt
        y = 175
        self.load_option_label = QtWidgets.QLabel(self.frame)
        self.load_option_label.setGeometry(QtCore.QRect(self.spacing_left+2, y, 150, 31))
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
        self.remove_system_btn.setEnabled(False)
        #Combobox_REMOVE_SELECTED_ITEM
        self.remove_selected_item_cbox = QtWidgets.QComboBox(self.frame)
        self.remove_selected_item_cbox.setGeometry(QtCore.QRect(self.spacing_left + 150, y+1, 150, 29))
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
        self.load_system_label.setGeometry(QtCore.QRect(self.spacing_left+4, 400, 150, 31))
        self.font.setPointSize(22)
        self.load_system_label.setText("Load system or Portfolio:")
        #SELECT_SYSTEM_CBOX
        self.loadDetails_selected_item_cbox = QtWidgets.QComboBox(self.frame)
        self.loadDetails_selected_item_cbox.setGeometry(QtCore.QRect(self.spacing_left + 150, 400, 150, 31))
        #Button_LOAD_DETAILS
        self.loadDetails_btn = QtWidgets.QPushButton(self.frame)
        self.loadDetails_btn.setGeometry(QtCore.QRect(self.spacing_left +300, 399, 150, 33))
        self.font.setPointSize(22)
        self.loadDetails_btn.setText("Load details")
        self.loadDetails_btn.setEnabled(False)
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
        self.openHelpFrame.triggered.connect(self.help_menu_btn_OnClick)
        #Action in combobox
        self.remove_selected_item_cbox.currentTextChanged.connect(self.__load_summary_trading_system__)       
    #ADD_SYSTEM_BUTTON_HANDLER
    def add_system_btn_Onclick(self):
        list_of_files = self.__file_manager__.get_files()
        for selected_file in list_of_files:
            #Add to portfolio
            ts_id = len(self.current_portfolio.trading_systems) + 1
            new_ts = TradingSystem(ts_id, selected_file)

            formatted_ts = self.format_duplicate(new_ts)

            self.current_portfolio.add_system(formatted_ts)
            self.current_portfolio.scalings.append(formatted_ts.volume) #Set the current volume in scaling list
            #add to combobox
            complete_item_name = str(str(formatted_ts.id) + " : " + str(formatted_ts.name))
            self.remove_selected_item_cbox.addItem(complete_item_name)
            if (self.loadDetails_selected_item_cbox.currentText() == ""):
                self.loadDetails_selected_item_cbox.addItem("0 : Portfolio")
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)
            else:
                self.loadDetails_selected_item_cbox.addItem(complete_item_name)    

            #Activate loading button
            self.loadDetails_btn.setEnabled(True)  
            self.remove_system_btn.setEnabled(True)
    #Check duplicated names in Ts list, change ts.name and every name in ts.trade_list
    def format_duplicate(self, new_ts):
        isDuplicate = False
        formatted_ts = deepcopy(new_ts)
        tss = TradingSystemSchema()
        label_index = tss.label_index_column
        if self.current_portfolio:
            for trading_system in self.current_portfolio.trading_systems:
                if formatted_ts.name == trading_system.name:
                    #La label di due ts è uguale
                    isDuplicate = True
                    break
                else:
                    #La label di due ts è diversa
                    isDuplicate = False    
        #Controllo se ho trovato il duplicato
        if isDuplicate:
            formatted_ts.name = str(new_ts.symbol) + "_" + str(new_ts.market) + str(random.randint(1, 99999))
            print("INFO: La label del trading system inserito è già presente nel portafogli. <", trading_system.name, ">")
            for trade in formatted_ts.trade_list:
                trade[label_index] = formatted_ts.name


        return formatted_ts  
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
            self.remove_selected_item_cbox.clear()
            #DeActivate loading button
            self.clear_portfolio_btn_Onclick()
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

        #Activate loading button
        self.loadDetails_btn.setEnabled(False)
        self.remove_system_btn.setEnabled(False)
    #Open Help frame
    def help_menu_btn_OnClick(self):
        hw = HelpWindow() 
        self.__secondary_windows__.append(hw)
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
                print("INFO: Trading system <", ts.name, "> will be load as portfolio component.")
                #for trade in self.current_portfolio.trading_systems[int(ID_instr_to_load)-1].trade_list:
                for trade in ts.trade_list:
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
            print("INFO: Portfolio scalings: ", self.current_portfolio.scalings)
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
        
        #for value in unordered_list_of_trades:
            #print(value)