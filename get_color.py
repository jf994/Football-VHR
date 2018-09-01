# il file gestisce il controllo sul colore del cartellino trovato (rosso o giallo)

import cv2
import numpy as np

# ritorna il numero di pixel nell'immagine che non sono neri
def count_nonblack_np(img):
    return img.any(axis=-1).sum()

# riconosce il colore
def detect_color(image, show=False):
    # definisco i boundaries per rosso e giallo
    boundaries = [
        ([0, 0, 153], [80, 80, 255]),  # rosso
        ([0, 204, 204], [102, 255, 255])  # giallo
    ]
    i = 0
    for (lower, upper) in boundaries:
        # creo array lower e upper dai boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # trovo il colore all'interno dei boundaries e applico la maschera
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)
        # calcolo la ratio tra i pixel che non sono neri del frame principale e di quello a cui ho applicato la maschera
        tot_pix = count_nonblack_np(image)
        color_pix = count_nonblack_np(output)
        ratio = color_pix / tot_pix
        # se la ratio è > .1 ed è il primo giro, ritorno 'red', altrimenti 'yellow'
        if ratio > 0.1 and i == 0:
            return 'red'
        elif ratio > 0.1 and i == 1:
            return 'yellow'

        i += 1
        # se show è true mostro l'immagine che ho selezionato
        if show == True:
            cv2.imshow("images", np.hstack([image, output]))

    return 'not_sure'