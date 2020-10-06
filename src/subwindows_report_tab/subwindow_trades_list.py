import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from trading_system import TradingSystem
print("Hello")

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# initialize the tkinter GUI
root = tk.Tk()

root.geometry("500x500")
root.pack_propagate(0)
root.resizable(0, 0)

# This is the frame for the Treeview
frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=250, width=500)

# This is the frame for the Open File dialog
file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=400, rely=0.65, relx=0)

button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)
button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)

label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

####
# THIS IS YOUR TABLE aka the TreeView widget
####
tv1 = ttk.Treeview(frame1)  # This is the Treeview Widget
column_list_account = ["Name", "Age", "Location"]  # These are our headings
tv1['columns'] = column_list_account  # We assign the column list to the widgets columns
tv1["show"] = "headings"  # this hides the default column..

for column in column_list_account:  # foreach column
    tv1.heading(column, text=column)  # let the column heading = column name
    tv1.column(column, width=50)  # set the columns size to 50px
tv1.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).
treescroll = tk.Scrollbar(frame1)  # create a scrollbar
treescroll.configure(command=tv1.yview)  # make it vertical
tv1.configure(yscrollcommand=treescroll.set)  # assign the scrollbar to the Treeview Widget
treescroll.pack(side="right", fill="y")  # make the scrollbar fill the yaxis of the Treeview widget

####


def File_dialog():
    """This function will open the file explorer"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    label_file.configure(text=filename)


def Load_excel_data():
    """ if your file is valid this will load the file into the treeview"""
    try:
        excel_filename = r"{}".format(label_file['text'])
        df = pd.read_excel(excel_filename)
    except ValueError:
        tk.messagebox.showerror("Information", "The File you have entered is invalid")
        return None

    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row)  # inserts each list into the treeview


root.mainloop()  # The mainloop for our tkinter Gui
