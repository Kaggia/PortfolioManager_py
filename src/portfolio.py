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
        self.scalings = []
        #Load Graphics
    #add a system to portfolio
    def add_system(self, ts):
        new_ts = ts
        self.trading_systems.append(new_ts)
        print("INFO: Trading system " + str(ts.name) + " added to Portfolio")
    #remove a system to portfolio NEED TO IMPLEMENT
    def remove_system(self, ts_id):
        self.trading_systems.pop(ts_id)
        print("INFO: Trading system <" + str(ts_id) + "> has been removed.")
    #Clear portfolio
    def clear(self):
        self.trading_systems = []
    #update whole list of scalings
    def update_scalings(self, list_of_updated_scalings):
        self.scalings = []
        for value in list_of_updated_scalings:
            self.scalings.append(float(value))
    #update single value of scalings
    def update_scaling_by_index(self, index, value):
        self.scalings[int(index)] = float(value)
        print("INFO: Scaling list is: ")
        print(self.scalings)
    #After deleting re-index the entire portfolio with new consistent indexes
    def indexing(self):
        id_progr = 1
        self.scalings = []
        for ts in self.trading_systems:
            ts.id = id_progr
            id_progr += 1
        for ts in self.trading_systems:
            self.scalings.append(ts.volume)
        print("INFO: Scaling list is: ")
        print(self.scalings)
