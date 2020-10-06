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
        self.state_checkbox_startDate = True
        self.state_checkbox_endDate = True
        self.state_radiobutton_custom = True
        self.state_radiobutton_realmoneygain = False

        self.isFirstApply = False    
        #Default Values
        self.startDate_d = Date (1, 1, 2000)
        self.endDate_d = Date (1, 1, 2000)
        self.time_window_d = 'd' 
    def setValues(self, _start_date, _end_date, _time_window, _guistate):
        self.startDate = _start_date
        self.endDate = _end_date
        self.time_window = _time_window
        
        self.state_checkbox_startDate = _guistate[0]
        self.state_checkbox_endDate = _guistate[1]
        self.state_radiobutton_custom = _guistate[2]
        self.state_radiobutton_realmoneygain = _guistate[3]

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
        print(self.state_checkbox_startDate)
        print(self.state_checkbox_endDate)
        print(self.state_radiobutton_custom)
        print(self.state_radiobutton_realmoneygain)
        print("----------------") 