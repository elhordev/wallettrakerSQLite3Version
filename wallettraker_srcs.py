
HEADER = "Wellcome to wallettraker v1.0 SQLite3 Version by elhorDev"
import os 
import pandas as pd
import time
import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup
import shutil
import keyboard
URL = "https://www.productoscotizados.com/mercado/ibex-35"
from colorama import Fore, Style

# Definir una función para aplicar el color del texto a una columna
def color_column(val):
    if val > 0:
        return Fore.GREEN + str(val) + Style.RESET_ALL
    elif val < 0:
        return Fore.RED + str(val) + Style.RESET_ALL
    else:
        return str(val)

