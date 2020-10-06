#Frame shows trades as tree views.

#Importing a parent file.py
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Scrollbar
import pandas as pd
from copy import deepcopy
from trading_system import TradingSystemSchema
class TradeListWindow:
    def __init__(self, _trade_list):
        self.trade_list = deepcopy(_trade_list)


        # initialize the tkinter GUI
        root = tk.Tk()

        root.geometry("500x500")
        root.pack_propagate(0)
        root.resizable(0, 0)

        # This is the frame for the Treeview
        frame1 = tk.LabelFrame(root, text="Portfolio Trades")
        frame1.place(height=500, width=500)

        self.tv1 = ttk.Treeview(frame1)  # This is the Treeview Widget
        tss = TradingSystemSchema()
        column_list_account = tss.__colums_checkList__  # These are our headings
        self.tv1['columns'] = column_list_account  # We assign the column list to the widgets columns
        self.tv1["show"] = "headings"  # this hides the default column..

        self.load_to_TreeView()

        
        for column in column_list_account:  # foreach column
            self.tv1.heading(column, text=column)  # let the column heading = column name
            self.tv1.column(column, width=100)  # set the columns size to 50px
        self.tv1.place(relheight=0.9, relwidth=0.95)  # set the height and width of the widget to 100% of its container (frame1).
        treescroll = tk.Scrollbar(frame1)  # create a scrollbar
        treescroll.configure(command=self.tv1.yview)  # make it vertical
        self.tv1.configure(yscrollcommand=treescroll.set)  # assign the scrollbar to the Treeview Widget
        hsb = Scrollbar(frame1, orient="horizontal", command=self.tv1.xview)
        hsb.place(relx=0.001, rely=0.9, relheight=0.10, relwidth=0.99)
        self.tv1.configure(xscrollcommand=treescroll.set)  # assign the scrollbar to the Treeview Widget
        treescroll.pack(side="right", fill="y")  # make the scrollbar fill the yaxis of the Treeview widget
        root.mainloop()  # The mainloop for our tkinter Gui
        ####
    def load_to_TreeView(self):
        #Get trade structure
        tss = TradingSystemSchema()
        df = pd.DataFrame(columns=tss.__colums_checkList__)
        list_of_df = []
        
        for row in self.trade_list:
            df_new = pd.DataFrame([row[:-1]], columns=tss.__colums_checkList__)
            list_of_df.append(df_new)

        df = pd.concat(list_of_df)
        df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            self.tv1.insert("", "end", values=row)  # inserts each list into the treeview



        
