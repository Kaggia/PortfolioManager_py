#Oggetto rappresentazione di una tab < report >
from PyQt5 import QtCore, QtGui, QtWidgets

#Instanciate and manage the report tab, printing all indexes
class ReportTab(QtWidgets.QTabWidget):
    def __init__(self,_columns, _rows, _spacingX, _spacingY):
        #Calling super <Tab>
        super().__init__()
        #<self> variable refers to the <Tab>
        self.rows = _rows  
        self.grid_counting = {"X": 0, "Y": 0}
        self.column_distancing = self.width() / (_columns * 2)
        self.positioning_cursor = {"X": 10, "Y": -20} #Posizione del cursore per il posizionamento
        self.spacing = {"X": _spacingX, "Y": _spacingY} #Spazio tra gli elementi
    #add a new index specifying <index_name> and his <value>
    def add_new_index(self, _index_name, _index_value):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        index_text_label = QtWidgets.QLabel(self)
        index_text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_text_label.setText(_index_name)
        #index_value
        index_value_label = QtWidgets.QLabel(self)
        index_value_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + self.spacing["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        index_value_label.setText(str(_index_value))
        self.__grid_counting__()
    #add a simple text
    def add_text(self, _text_to_show):
        #positioning in a new line
        self.positioning_cursor["Y"] += self.spacing["Y"]
        #index_text
        text_label = QtWidgets.QLabel(self)
        text_label.setGeometry(QtCore.QRect(self.positioning_cursor["X"] + (self.column_distancing * self.grid_counting["Y"]), 
                                                        self.positioning_cursor["Y"], 
                                                         150, 
                                                          30)
                                            )
        text_label.setText(_text_to_show)
        self.__grid_counting__()
    #when you add a row, manage the colums
    def __grid_counting__(self):
        self.grid_counting["X"] += 1
        if self.grid_counting["X"] > self.rows :
            #si è superato il limite di righe
            self.grid_counting["X"] = 0
            self.grid_counting["Y"] += 1
            #Reset cursor for Y
            self.positioning_cursor["Y"] = -20