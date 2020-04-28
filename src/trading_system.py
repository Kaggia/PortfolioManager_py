#trading_system.py
#Define the structure of a Trading system
#Libraries
import pandas as pd
class TradingSystem:
    def __init__(self, ts_filepath):
        #Attributes
        self.id = None
        self.name = None
        self.symbol = None
        self.trade_list = None
        self.indexes = None 
        self.__colums_checkList__ = ['Closing Deal ID', 'Label', 'Symbol', 'Net €']
        #Elaboration
        self.__load_data_from_csv__(ts_filepath)
    #scan a csv file, getting data from it
    def __load_data_from_csv__(self, filepath):
        if self.__check_file_integrity__(filepath):
            print("INFO: CSV is valid, ready to load.")
            #Load_id
            #Load_name
            #Load_symbol
            #Load_TRADE_LIST
            row = []
            self.trade_list = []
            pd_dataframe = pd.read_csv(filepath)
            i = 0        
            for _ in range(len(pd_dataframe)):
                for column in self.__colums_checkList__:
                    row.append(pd_dataframe.at[i, column])
                self.trade_list.append(row)
                row = []
                i += 1
        else:
            print("ERROR: CSV is NOT valid, please select a VALID one.")
    #check integrity of a file CSV        
    def __check_file_integrity__(self, ts_filepath):
        print("INFO: Reading CSV in -> " + str(ts_filepath))
        pd_dataframe = pd.read_csv(ts_filepath)
        pd_columns = pd_dataframe.columns
        integrity = True
        for column_to_check in self.__colums_checkList__:
            if column_to_check in pd_columns:
                #la colonna è presente
                pass
            else:
                integrity = False
                print("ERROR: Column <" + column_to_check + "> is not a valid column") 
                break       
        return integrity
    #Print trades on console
    def print_trade_list(self):
        for row in self.trade_list:
            print(row)
            print("")