#indexes.py
#il modulo raccoglie tutti gli indici, ed i metodi per calcolarli

#Define an interface
class CustomIndex():
    def __init__(self, _tradeList):
        self.__trade_list__ = _tradeList
        self.value = None
    #calculate and return the index
    def calculate(self):
        pass
#Calculate the equity (final) <NOT_IMPLEMENTED>
class Equity(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = 0
        return value
#Extract name of Trading system or set to Portfolio
class Name(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = ""
        tl = self.__trade_list__
        tl_first = tl[0]
        prev_ts_name = tl_first[1] #prende il nome del ts 
        #check if it is a portfolio or a system
        for trade in self.__trade_list__:
            ts_name = trade[2]
            if not(prev_ts_name == ts_name):
                #It's a portfolio
                value = "Portfolio"
                break
            else:
                value = ts_name
        return value
#Extract Symbol of Trading system (Formatted to fit the name of ts)
class FormattedSymbol(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = ""
        temp_name = Name(self.__trade_list__)

        if(temp_name.calculate() == "Portfolio"):
            value = ""
        else:
            tl = self.__trade_list__
            tl_first = tl[0]
            value = " - " + tl_first[2] #prende il nome del ts     
        return value
#Extract Symbol of Trading system
class Symbol(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = ""
        temp_name = Name(self.__trade_list__)

        if(temp_name.calculate() == "Portfolio"):
            value = ""
        else:
            tl = self.__trade_list__
            tl_first = tl[0]
            value = tl_first[2] #prende il nome del ts     
        return value
        
