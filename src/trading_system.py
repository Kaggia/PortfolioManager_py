#trading_system.py
#Define the structure of a Trading system
#Libraries
import pandas as pd
from os_interactors import FileManager
class TradingSystem:
    def __init__(self,_id, ts_filepath):
        #Attributes
        self.id = _id
        self.name = None
        self.symbol = None
        self.trade_list = None
        self.indexes = None 
        self.__colums_checkList__ = ['Closing Deal ID', 'Label', 'Symbol', 'Volume', 'Close Time', 'Net']
        #Elaboration
        self.__clear_columns_name__(ts_filepath)
        self.__clear_columns_name__(ts_filepath)
        self.__load_data_from_csv__(ts_filepath) 
        self.volume = self.get_volume_as_fraction() #float   
    #scan a csv file, getting data from it
    def __load_data_from_csv__(self, filepath):
        if self.__check_file_integrity__(filepath):
            print("INFO: CSV is valid, ready to load.")
            #Load_TRADE_LIST
            row = []
            self.trade_list = []
            pd_dataframe = pd.read_csv(filepath, encoding='latin-1')
            i = 0        
            for _ in range(len(pd_dataframe)):
                for column in self.__colums_checkList__:
                    row.append(pd_dataframe.at[i, column])
                self.trade_list.append(row)
                row = []
                i += 1
            #Load_name
            if self.trade_list:
                first_row = self.trade_list[0]
                self.name = first_row[1]
                #Load_symbol
                self.symbol = first_row[2]
            #Convertion date from <IT> to <ENG> format
            if self.__detect_date_format__() == 0:
                #Date format is NOT English
                self.__date_convertion__()
        else:
            print("ERROR: CSV is NOT valid, please select a VALID one.")
    #check integrity of a file CSV        
    def __check_file_integrity__(self, ts_filepath):
        print("INFO: Reading CSV in -> " + str(ts_filepath))
        pd_dataframe = pd.read_csv(ts_filepath, encoding='latin-1')
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
    #clear the first line (colum_names), cause some of them are inconsistent
    def __clear_columns_name__(self, ts_filepath):
        #CLEAR dates(UTC+n) part
        with open(ts_filepath) as f:
            lines = f.readlines()
        
        lines[0] = "Closing Deal ID,Label,Entry Time,Symbol,Volume,Type,Entry Price,Commissions,Close Price,Close Time,Net,Gross\n"

        with open(ts_filepath, "w") as f:
            f.writelines(lines)
    #detect what format of date is
    def __detect_date_format__(self):
        date_format = 1 #English
        for trade in self.trade_list:
            for column in trade:
                if len(str(column)) == 16:
                    if (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                        should_month = int(column[0:2])
                        if should_month > 12 :
                            date_format = 0
                            print("INFO: Date format detected is <IT>. It will be changed to <ENG>")
                            return date_format
        print("INFO: Date format detected is <ENG>")
        return date_format
    #convert date format
    def __date_convertion__(self):
        converted_trade_list = []
        trade = []
        for trade in self.trade_list:
            trade_converted = []
            for column in trade:
                if len(str(column)) == 16:
                    if (column[2] == "/") and (column[5] == "/") and (column[13] == ":") :
                        swap = ""
                        should_month = column[0:2]
                        should_day = column[3:5]
                        swap = should_month
                        should_month = should_day
                        should_day = swap
                        year = column[6:11]
                        hour = column[11:13]
                        minutes = column[14:]
                        correct_date = should_month + "/" + should_day + "/" + year + "" + hour + ":" + minutes
                        trade_converted.append(correct_date)
                    else:
                        trade_converted.append(column)
                else:
                    trade_converted.append(column)
            converted_trade_list.append(trade_converted)
        self.trade_list = converted_trade_list
    #Detect current fraction of volume, and get it as float
    def get_volume_as_fraction(self):
        #dict_of_scales = {'k' : 0.01, 'm': 10}
        value_volume = 0
        volume_index = self.__colums_checkList__.index('Volume')
        first_raw_volume = self.trade_list[0][volume_index] 
        #check for integrity of volume
        isInt = True
        for trade in self.trade_list:
            if trade[volume_index] != first_raw_volume:
                print("ERROR: Volume detected changes during the trading.")
                isInt = False
        if isInt:
            clean_volume = first_raw_volume[first_raw_volume.rfind(" ")+1:]
            if clean_volume[-1] == 'k':
                value_volume = float(clean_volume [:-1]) / 100
                print("INFO: Volume as fraction is-> " + str(value_volume))
            else:
                print("WARNING: High volume(Million) detected, check implementation.")
                value_volume = float(clean_volume [:-1]) * 10
                print("INFO: Volume as fraction is-> " + str(value_volume))
        return value_volume
    #Print trades on console
    def print_trade_list(self):
        for row in self.trade_list:
            print(row)
            print("")