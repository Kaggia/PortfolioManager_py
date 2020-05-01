#indexes.py
#il modulo raccoglie tutti gli indici, ed i metodi per calcolarli

class CustomIndex():
    def __init__(self, _tradeList):
        self.__trade_list__ = _tradeList
        self.value = None
    #calculate and return the index
    def calculate(self):
        pass
class Equity(CustomIndex):
    #calculate and return the index
    def calculate(self):
        value = 0
        return value