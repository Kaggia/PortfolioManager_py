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
    def add_system(self, ts):
        new_ts = ts
        self.trading_systems.append(new_ts)
        print("INFO: Trading system " + str(ts.name) + " added to Portfolio")
    #remove a system to portfolio NEED TO IMPLEMET
    def remove_system(self, ts_id):
        self.trading_systems.pop(ts_id)
        print("INFO: Trading system <" + str(ts_id) + "> has been removed.")
    #Clear portfolio
    def clear(self):
        self.trading_systems = []