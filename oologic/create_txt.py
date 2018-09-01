# nel file sono presenti le funzioni per gestire la stampa del json finale
import os


# la funzione prende in ingresso alcuni parametri come il nome della cartella e il nome del file txt, li crea se non
# esistono e infine scrive il txt utilizzando i dati contenuti nella variabile data
def writeToTXTFile(dir, fileName, data):
    filePathNameWExt = './' + dir + '/' + fileName + '.txt'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(filePathNameWExt, 'w') as fp:
        fp.write(data)
