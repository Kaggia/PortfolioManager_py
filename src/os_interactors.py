#os_interactor.py
#Modulo per le interazioni con il sistema operativo

#Libraries
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askopenfilename

class FileManager:
    def __init__(self):
        pass
    #restituisce i filepaths dei files, ottenuti mediante explorer
    def get_files(self, allowed_extension='csv'):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filenames = askopenfilenames(title = "Select a single history or a group (." + allowed_extension +")", filetypes = (("csv files","*." + allowed_extension),("all files","*.*"))) 
        return filenames
    #salva un file, nella cartella di destinazione specificata <NOT_IMPL>
    def save_file(self, completePath):
        pass
    def dump_list_of_list(self, complete_path, listToDump):
        sum_of_text = ""
        txt_file = open(complete_path, "w")
        for m_elem in listToDump:
            for s_elem in m_elem:
                sum_of_text = sum_of_text + str(s_elem) + "\n"
            txt_file.write(sum_of_text)
            sum_of_text = ""
