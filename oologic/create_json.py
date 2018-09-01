# nel file sono presenti le funzioni per gestire la stampa del json finale

import json
import os
import sys

# la funzione prende in ingresso alcuni parametri come il nome della cartella e il nome del file json, li crea se non
# esistono e infine scrive il json utilizzando i dati contenuti nella variabile data

def writeToJSONFile(dir, file_name, data):
    filePathNameWExt = './' + dir + '/' + file_name + '.json'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
