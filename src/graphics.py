#graphics.py
#Libreria grafica contenente gli oggetti dell'interfaccia
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import os

class MainWindow:
    def __init__(self):
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(1024, 720)
        self.frame.setWindowTitle("cTrader - Portfolio Manager")
        self.frame.setMinimumSize(QtCore.QSize(720, 480))
        self.frame.setMaximumSize(QtCore.QSize(720, 480))

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
        
        #logo
        #self.logoLabel = QtWidgets.QLabel(self.frame)
        #self.logoLabel.setGeometry(QtCore.QRect(422, 10, 180, 160))
        #self.logoLabel.setPixmap(QtGui.QPixmap(os.path.join(directory.IMGS_FOLDER, "logo.png")))

        self.frame.show()
