#graphics.py
#Libreria grafica contenente gli oggetti dell'interfaccia
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import os
#My Modules
import CONSTANTS as directory

class MainWindow:
    def __init__(self):
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(1024, 720)
        self.frame.setWindowTitle("cTrader - Portfolio Manager")
        self.frame.setMinimumSize(QtCore.QSize(720, 480))
        self.frame.setMaximumSize(QtCore.QSize(720, 480))
        self.font = QtGui.QFont()
        self.spacing_left = 25

        self.__load_menu_bar__()
        self.__load_loading_options__()
        self.__add_separator__()
        self.__load_selecting_system__()
        #logo
        self.logoLabel = QtWidgets.QLabel(self.frame)
        self.logoLabel.setGeometry(QtCore.QRect(250, 10, 200, 175)) #(posX, posY, dimX, dimY)
        self.logoLabel.setPixmap(QtGui.QPixmap(os.path.join(directory.RESOURCE_FOLDER, "logo.png")))

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
    #Load the section relative to loading options
    def __load_loading_options__(self):
        #Label_loading_opt
        y = 175
        self.load_option_label = QtWidgets.QLabel(self.frame)
        self.load_option_label.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.load_option_label.setText("Load options:")

        #Button_LOAD_NEW_PF
        y += 25
        self.load_new_portfolio_btn = QtWidgets.QPushButton(self.frame)
        self.load_new_portfolio_btn.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.load_new_portfolio_btn.setText("Load Portfolio(Folder)")
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
        self.remove_selected_item_cbox.addItem("ITEM_SELECTED")
        #Button_CLEAR_PORTFOLIO
        y += 35
        self.clear_portfolio_btn = QtWidgets.QPushButton(self.frame)
        self.clear_portfolio_btn.setGeometry(QtCore.QRect(self.spacing_left, y, 150, 31))
        self.font.setPointSize(22)
        self.clear_portfolio_btn.setText("Clear Portfolio")
    #Define a separator, based on png file
    def __add_separator__(self):
        self.logoLabel = QtWidgets.QLabel(self.frame)
        self.logoLabel.setGeometry(QtCore.QRect(100, 350, 500, 10)) #(posX, posY, dimX, dimY)
        self.logoLabel.setPixmap(QtGui.QPixmap(os.path.join(directory.RESOURCE_FOLDER, "separator.png")))
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
        self.loadDetails_selected_item_cbox.addItem("ITEM_SELECTED")
        #Button_LOAD_DETAILS
        self.loadDetails_btn = QtWidgets.QPushButton(self.frame)
        self.loadDetails_btn.setGeometry(QtCore.QRect(self.spacing_left +300, 400, 150, 31))
        self.font.setPointSize(22)
        self.loadDetails_btn.setText("Load details")
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