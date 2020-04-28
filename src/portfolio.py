#portfolio.py
#Definisce la classe per la gestione del portafogli
#Libraries

#My Modules
from trading_system import TradingSystem
from os_interactors import FileManager
class Portfolio:
    def __init__(self):
        self.trading_systems = []
        self.indexes = None
        #Load Graphics
    #add a system to portfolio
    def add_system(self, filepath):
        fm = FileManager()
        for path in fm.get_files():
            ts = TradingSystem(path)
            self.trading_systems.append(ts)
            print("INFO: Trading system " + str(ts.name) + " added to Portfolio")
    #remove a system to portfolio
    def remove_system(self, ts_id):
        pass