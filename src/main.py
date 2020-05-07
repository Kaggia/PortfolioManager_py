#main.py
#Modulo principale per il lancio dell'applicazione
#C:\Users\zimmi\Documents\vsCode\PortfolioManager_py\data\portfolio_test
#Libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
#My Modules
from app import MainWindow, DetailWindow
from os_interactors import FileManager
from trading_system import TradingSystem
from portfolio import Portfolio

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #Create a portfolio NONE
    p = Portfolio()
    #Create main window
    mw = MainWindow(p)
    #SET_EXIT
    sys.exit(app.exec_())


