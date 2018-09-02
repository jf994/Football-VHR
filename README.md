# TRANSACTIONAL SYSTEM AND DATA WAREHOUSES - Football highlights

## Progetto a cura di Fabrizio Zavanone e Jacopo Favaro

<p align="center"> <img src="https://github.com/jf994/Football-VHR/tree/master/docs/test2.gif"/> </p>

### Intro

Sistema di estrapolazione di informazioni da un video di una partita di calcio con layout sky del mondiale 2006. Paper: (LINKPAPER)

### Dipendenze

Python3, tensorflow 1.0, numpy, opencv 3.

### Come iniziare

Installare con pip darkflow globalmente, usando il comando
    ```
    pip install -e .
    ```
    
### Preparazione nuovo modello

Nella cartella img_download/google_images_download sono presenti i file necessari per eseguire uno script python che permette di scaricare immagini in buona risoluzione da google (rifarsi al readme presente nella cartella).

La cartella creatasi con le immagini deve essere spostata in img_download/google_images_download/downloads e le immagini scaricate devono poi essere rinominate tramite lo script `rename.py`, ivi presente, che le sposterà, rinominandole, nella cartella train_images.
Tale cartella deve essere poi essere trasferita in new_model_data, per essere utilizzata al fine di generare le annotazioni attraverso l'esecuzione dello script `draw_box.py` (modificare il contenuto dello script secondo necessità per includere le classi desiderate).

Un video tutorial su cui ci siamo basati per questo progetto può essere trovato [qui](https://www.youtube.com/watch?v=Fwcbov4AzQo&list=PLX-LrBk6h3wSGvuTnxB2Kj358XfctL4BM&index=6) e nel [successivo](https://www.youtube.com/watch?v=2XznLUgj1mg&index=7&list=PLX-LrBk6h3wSGvuTnxB2Kj358XfctL4BM).
 
### Trainare un nuovo modello

*Le informazioni seguenti assumono che si voglia utilizzare tiny YOLO e il dataset contenga 2 classi*

1. Creare una copia del configuration file `tiny-yolo-voc.cfg` e rinominarlo seguendo le proprie preferenze `tiny-yolo-voc-2c.cfg` (dove il 2c sta per 2 classi) (è importante lasciare il file originale `tiny-yolo-voc.cfg` invariato per succiessive modifiche, vedi spiegazione successiva).

2. In `tiny-yolo-voc-2c.cfg`, modificare il numero classes nel layer [region] (l'ultimo layer) facendolo corrispondere al numero di classi sulle quali si sta per trainare la rete (nel nostro caso 2):
    
    ```python
    ...

    [region]
    anchors = 1.08,1.19,  3.42,4.41,  6.63,11.38,  9.42,5.11,  16.62,10.52
    bias_match=1
    classes=2
    coords=4
    num=5
    softmax=1
    
    ...
    ```

3. In `tiny-yolo-voc-2c.cfg`, cambiare il numero filters nel layer [convolutional] (penultimo layer) in num * (classes + 5). Nel nostro caso, num è 5 e classes 2 quindi 5 * (2 + 5) = 35 quindi filters è settato a 35:
    
    ```
    python
    ...

    [convolutional]
    size=1
    stride=1
    pad=1
    filters=35
    activation=linear

    [region]
    anchors = 1.08,1.19,  3.42,4.41,  6.63,11.38,  9.42,5.11,  16.62,10.52

    ...
    ```

4. Cambiare `labels.txt` per includere i label sui quali si desidera trainare la rete (il numero dei label deve essere lo stesso del numero delle classi settate nel file `tiny-yolo-voc-2c.cfg`). Nel nostro caso, `labels.txt` conterrà 2 label:

    ```
    label1
    label2
    ```
5. Al momento di trainare rimanda al modello `tiny-yolo-voc-2c.cfg`, eseguendo il seguente comando:

    `python flow --model cfg/tiny-yolo-voc-2c.cfg --load bin/tiny-yolo-voc.weights --train --annotation new_model_data/annotations --dataset new_model_data/train_images --gpu 1.0 --epoch 600`
    
`Per caricare il training da un determinato punto, dopo load mettere il numero del checkpoint desiderato invece di bin/tiny-yolo-voc.weights`


* Perchè lasciare il file `tiny-yolo-voc.cfg` invariato?
    
   Quando darkflow vede che si desidera caricare `tiny-yolo-voc.weights` cercerà `tiny-yolo-voc.cfg` nella cartella cfg/ del progetto comparando quel file di configurazione con il nuovo settato da te `--model cfg/tiny-yolo-voc-2c.cfg`. In questo caso ogni layer avrà lo stesso numero per i pesi eccetto per gli ultimi 2 così da caricare i pesi dentro tutti i layer sino agli ultimi due dato che questi ultimi sono stati cambiati

### Eseguire l'analisi video in tempo reale

Modificare il file `options.csv` inserendo i seguenti dati separati da virgola:


    ```
    path relativo del video desiderato, threshold per darknet (valore tra zero e uno, l'analisi è stata testata per 0.55), numero checkpoint raggiunto durante il training, framerate del video originale
    ```
Modificare il file `crops_value.csv` inserendo i seguenti dati come mostrato:


    ```
    55,70,YMIN&YMAX
    225,385,X'sTABELLONE
    284,300,X'sHOME
    312,328,X'sGUEST
    ``
* riga 1 rappresenta i valori Ymin e Ymax per tutti i crop
* riga 2 rappresenta le coordinate Xmin e Xmax del tabellone intero
* riga 3 rappresenta le coordinate Xmin e Xmax del punteggio della squadra di casa
* riga 4 rappresenta le coordinate Xmin e Xmax del punteggio della squadra ospite

Modificare nella cartella oologic il file `template.csv` inserendo i seguenti dati separati da virgola:


    ```
    data espressa nel formato AAMMGG, sport, campionato, numero partita
    ```
Modificare nella cartella oologic il file csv relativo alla squadra home e nominaro nomesquadracasa.csv inserendo i dati come mostrato nel file di dimostrazione `italy.csv` :


    ```
    Italy
    Lippi,CT
    Buffon,1,P,Gold,False
    Grosso,3,DS,Azur,False
    Cannavaro,5,DC,Azur,True
    Gattuso,8,CC,Azur,False
    Toni,9,ATT,Azur,False
    Totti,10,AT,Azur,False
    Camoranesi,16,ED,Azur,False
    Zambrotta,19,TD,Azur,False
    Perrotta,20,ES,Azur,False
    Pirlo,21,CC,Azur,False
    Materazzi,23,DC,Azuz,False
    Zaccardo,2,DC,Azur,False
    De Rossi,4,CC,Azur,False
    Barzagli,6,DC,Azur,False
    Del Piero,7,AT,Azur,False
    Gilardino,11,ATT,Azur,False
    Peruzzi,12,P,Gold,False
    Nesta,13,DC,Azur,False
    Amelia,14,P,Gold,False
    Iaquinta,15,ATT,Azur,False
    Barone,17,CC,Azur,False
    Inzaghi,18,ATT,Azur,False
    Oddo,22,TD,Azur,False

    ```
    
ATTENZIONE: l'ordine degli elementi del file non è casuale e deve essere rispettato 

    ```
    Nome squadra
    Nome Allenatore,CT
    Giocatori titolari in ordine di numero
    Giocatori in panchina in ordine di numero

    ```
per ogni giocatore dovrà essere specificato: Cognome giocatore, numero, ruolo, colore maglia, booleano True se è capitano False altrimenti

La stessa procedura dovrà essere ripetuta per la squadra ospite

Modificare nella cartella oologic il file csv `match.csv` inserendo i seguenti dati:

    ```
    nome del file csv creato per la squadra di casa, nome del file csv creato per la squadra ospite
    Cognome arbitro, REF, Colore Maglia

    ```
    
Inserire nella cartella img tre cartelle. Le prime due dovranno chiamarsi come la squadra di riferimento è stata chiamata nel file csv e dovranno altresì contenere un'immagine per giocatore e allenatore presente nel suddetto csv. Le immagini dovranno inoltre rispettare la nomenclatura sin ora seguita nel file. L'ultima cartella dovra chiamarsi 'Ref' e contenere un'immagine per l'arbitro denominata come spiegato in precedenza.

Infine, da terminale, raggiungere la cartella del progetto e digitare il seguente comando:

    `python processing_video.py`
