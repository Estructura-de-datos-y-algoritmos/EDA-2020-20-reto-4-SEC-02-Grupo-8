import config as cf
import os

import csv

def loadFile():
    print("hlskdxnj")
    
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            #loadData(analyzer, filename)
    return None

def prueba():
    print("hpññs")


loadFile()