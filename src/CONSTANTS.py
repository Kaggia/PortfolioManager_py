#CONSTANTS.py
#La classe definisce alcune costanti per il progetto.
import os
import getpass
from pathlib import Path
#Cartelle interessanti per il progetto
cwd = os.getcwd()
RESOURCE_FOLDER = cwd + "/PortfolioManager_py/resource/"
SRC_FOLDER = cwd + "/PortfolioManager_py/src/"
DATA_FOLDER = cwd + "/PortfolioManager_py/data/"

if __name__ == "__main__":
    print(RESOURCE_FOLDER)
    print(SRC_FOLDER)
    print(DATA_FOLDER)
    