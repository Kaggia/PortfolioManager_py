#main.py
#Modulo principale per il lancio dell'applicazione

#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
#My Modules
from graphics import MainWindow, DetailWindow
from os_interactors import FileManager

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    #Create main window
    #mw = MainWindow()
    #dw = DetailWindow()
    fm = FileManager()
    #SET_EXIT
    sys.exit(app.exec_())
