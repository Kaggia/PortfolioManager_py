#graphics.py
#Libreria grafica contenente gli oggetti dell'interfaccia
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import os
#My Modules
import CONSTANTS as directory
from os_interactors import FileManager
from trading_system import TradingSystem

class MainWindow:
    def __init__(self, _portfolio):
        self.current_portfolio = _portfolio
        self.__file_manager__ = FileManager()
        
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
class DetailWindow:
   #load equity tab
    def __init__(self):
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(720, 480)
        self.frame.setWindowTitle("cTrader - Portfolio Manager - Detail window")
        self.frame.setMinimumSize(QtCore.QSize(720, 480))
        self.frame.setMaximumSize(QtCore.QSize(720, 480))
        self.font = QtGui.QFont()
        
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget(self.frame)
        self.tab_report = QtWidgets.QWidget()
        self.tab_drawdown = QtWidgets.QWidget()
        self.tab_equity = QtWidgets.QWidget()
        self.tabs.resize(300,200)
        # Add tabs
        self.tabs.addTab(self.tab_report,"Tab Report")
        self.tabs.addTab(self.tab_drawdown,"Tab Drawdown")
        self.tabs.addTab(self.tab_equity,"Tab Equity")

        self.frame.show()
    #load equity tab
    def __tab_report_loader__(self):
        pass
    #load equity tab
    def __tab_drawdownChart_loader(self):
        pass
    #load equity tab
    def __tab_equity_loader(self):
        pass