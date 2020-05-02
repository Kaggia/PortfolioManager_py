#graphics.py
#Libreria grafica contenente gli oggetti dell'interfaccia
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from operator import itemgetter
import os
#My Modules
import CONSTANTS as directory
from os_interactors import FileManager
from trading_system import TradingSystem
#Main window where you can manage the whole portfolio
class MainWindow:
    def __init__(self, _portfolio):
        self.current_portfolio = _portfolio
        self.__file_manager__ = FileManager()
        self.__secondary_windows__ = []
        
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
   #load equity tab
    def __init__(self, _unordered_list_of_trades):
        self.trades = _unordered_list_of_trades
        self.__order_raw_trade_list__()
        
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
        self.tabs.resize(500,400)
        # Add tabs
        self.tabs.addTab(self.tab_report,"Tab Report")
        self.tabs.addTab(self.tab_drawdown,"Tab Drawdown")
        self.tabs.addTab(self.tab_equity,"Tab Equity")
        #Load Tabs content
        self.__tab_report_loader__()
        self.__tab_equity_loader()
        self.__tab_drawdownChart_loader()

        self.frame.show()
    #load equity tab
    def __tab_report_loader__(self):
        #Instanciate a scrolling area with <n, m> grid
        scrolling_grid_area = ScrolligGridArea(self.tab_report, 2, 5, 50, 25)

    #load equity tab
    def __tab_drawdownChart_loader(self):
        pass
    #load equity tab
    def __tab_equity_loader(self):
        pass
    #order tradelist passed
    def __order_raw_trade_list__(self):
        #itemgetter_0->ID
        #itemgetter_1->Label
        #etc...
        ordered_list = sorted(self.trades, key=itemgetter(0))
        self.trades = ordered_list
        for trade in self.trades:
            print(trade)
#Describe an area where indexes can be added, row by row
class ScrolligGridArea():
    def __init__(self, _widget, _columns, _rows, _spacingX, _spacingY):
        self.columns = _columns #Colonnee intese come coppia <Label, label>
        self.rows = _rows  
        self.height = _widget.height()
        self.width = _widget.width()
        self.positioning_cursor = {"X": 0, "Y": 0}
        self.spacing = {"X": _spacingX, "Y": _spacingY}

        self.parent = _widget
        self.scroll = QtWidgets.QScrollArea(self.parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.parent.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(QtCore.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.parent)

        self.parent.setCentralWidget(self.parent)
    #add a new index specifying <index_name> and his <value>
    def add_new_index(self, _index_name, _index_value):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        index_text_label = QtWidgets.QLabel()
        index_text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"], 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_text_label.setText(_index_name)
        #index_value
        index_value_label = QtWidgets.QLabel()
        index_value_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + self.spacing["X"], 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_value_label.setText(_index_value)
        #add to layout
        self.vbox.addWidget(index_text_label)
        self.vbox.addWidget(index_value_label)
    #add a new line of text like it was a couple <index_name> and his <value>
    def add_text(self, _text_to_show):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        text_label = QtWidgets.QLabel()
        text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"], 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        text_label.setText(_text_to_show)
        #add to layout
        self.vbox.addWidget(text_label)
