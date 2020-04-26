#trading_system.py

class TradingSystem:
    def __init__(self, ts_filepath):
        self.id = None
        self.name = None
        self.symbol = None
        self.trade_list = None
        self.indexes = None 
        pass
    #scan a csv file, getting data from it
    def __load_data_from_csv__(self):
        pass