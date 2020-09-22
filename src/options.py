#options.py
#Definiamo una classe in cui raccogliere un immagine delle opzioni
from PyQt5 import QtCore, QtGui, QtWidgets

class Option:
    def __init__(self, _start_date=None, _end_date=None):
        #Mockup
        self.startDate = QtCore.QDate (1, 1, 2000)
        self.endDate = QtCore.QDate (1, 1, 2000)
        self.time_window = 'd'

        self.isFirstApply = False    
        #Default Values
        self.startDate_d = QtCore.QDate (1, 1, 2000)
        self.endDate_d = QtCore.QDate (1, 1, 2000)
        self.time_window_d = 'd' 
    def setValues(self, _start_date, _end_date, _time_window):
        print("Date inside s: ", _start_date.toString())
        print("Date inside e: ", _end_date.toString())
        self.startDate = _start_date
        self.endDate = _end_date
        self.time_window = _time_window

        self.__set_default_values__()
    def __set_default_values__(self):
        if self.isFirstApply == False :
            self.isFirstApply = True
            self.startDate_d = self.startDate
            self.endDate_d = self.endDate
            self.time_window_d = self.time_window