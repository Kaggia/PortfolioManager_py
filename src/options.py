#options.py
#Definiamo una classe in cui raccogliere un immagine delle opzioni
from PyQt5 import QtCore, QtGui, QtWidgets

from date import Date

class Option:
    def __init__(self, _start_date=None, _end_date=None):
        #Mockup
        self.startDate = Date (1, 1, 2000)
        self.endDate = Date (1, 1, 2000)
        self.time_window = 'd'

        self.isFirstApply = False    
        #Default Values
        self.startDate_d = Date (1, 1, 2000)
        self.endDate_d = Date (1, 1, 2000)
        self.time_window_d = 'd' 
    def setValues(self, _start_date, _end_date, _time_window):
        self.startDate = _start_date
        self.endDate = _end_date
        self.time_window = _time_window

        self.__set_default_values__()
        self.__printInfo__()
    def __set_default_values__(self):
        if self.isFirstApply == False :
            self.isFirstApply = True
            self.startDate_d = self.startDate
            self.endDate_d = self.endDate
            self.time_window_d = self.time_window
    def __printInfo__(self):
        print("----------------") 
        print("Options saved:") 
        print(str(self.startDate.d), " ", str(self.startDate.m), " ", str(self.startDate.y ))
        print(str(self.endDate.d), " ", str(self.endDate.m), " ", str(self.endDate.y) )   
        print(self.time_window)
        print("----------------") 