#trading_system.py
#Define the structure of a Trading system
#Libraries
import pandas as pd
class TradingSystem:
    def __init__(self,_id, ts_filepath):
        #Attributes
        self.id = _id
        self.name = None
        self.symbol = None
        self.trade_list = None
        self.indexes = None 
        self.__colums_checkList__ = ['Closing Deal ID', 'Label', 'Symbol', 'Close Time (UTC+1)', 'Net €']
        #Elaboration
        self.__clear_columns_name__(ts_filepath)
        self.__load_data_from_csv__(ts_filepath)
    #scan a csv file, getting data from it
    def __load_data_from_csv__(self, filepath):
        if self.__check_file_integrity__(filepath):
            print("INFO: CSV is valid, ready to load.")
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
            #Load_name
            if self.trade_list:
                first_row = self.trade_list[0]
                self.name = first_row[1]
                #Load_symbol
                self.symbol = first_row[2]
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
    #clear the first line (colum_names), cause some of them are inconsistent
    def __clear_columns_name__(self, ts_filepath):
        #CLEAR dates(UTC+n) part
        with open(ts_filepath) as f:
            lines = f.readlines()
        #Find (UTC+) part, and subs it
        first_line = lines[0]
        first_line_first_part = first_line[:first_line.find("(UTC+")-1]
        first_line_second_part = first_line[first_line.find("(UTC+") + 7:]
        good_line = first_line_first_part + first_line_second_part
        first_line = good_line
        first_line_first_part = first_line[:first_line.find("(UTC+")-1]
        first_line_second_part = first_line[first_line.find("(UTC+") + 7:]
        good_line = first_line_first_part + first_line_second_part
        lines[0] = good_line
        with open(ts_filepath, "w") as f:
            f.writelines(lines)

    #Print trades on console
    def print_trade_list(self):
        for row in self.trade_list:
            print(row)
            print("")