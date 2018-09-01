# nel file è presente la funzione che permette di leggere il csv che contiene le informazioni da inserire nel dizionario
# 'options' del file principale processing_video.py
import csv

def get_opt():
    with open('options.csv', 'r') as f:
        reader = csv.reader(f)
        array = list(reader)[0]

        return array

