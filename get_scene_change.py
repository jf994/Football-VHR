# il file controlla l'avvenuto (o meno) cambio di scena

import cv2
import numpy as np


# calcolo la distanza tra le ratio attraverso la funzione chi-squared distance e ritorno le nuove ratio a cui appendo
# la distanza calcolata
def count_distance(old_ratio, new_ratio):

    i = 0
    val = 0
    for ratio in old_ratio:
        if (ratio + new_ratio[i] != 0):
            val += ((ratio - new_ratio[i]) ** 2)/(ratio + new_ratio[i])
        i += 1

    val *= 2
    new_ratio.append(val)
    return new_ratio


# conto il numero di pixel nell'immagine che non sono neri
def count_nonblack_np(img):
    return img.any(axis=-1).sum()

# calcola le ratio dei valori RGB
def is_new_scene(image, old_ratio, do_resize):
    red_ratio = 0
    blue_ratio = 0
    green_ratio = 0
    small_frame = image

    if do_resize:
        small_frame = cv2.resize(image, (0, 0), fx=0.1, fy=0.1)

    # definisco i boundaries
    boundaries = [
        ([0, 0, 153], [80, 80, 255]),  # red
        ([86, 31, 4], [220, 88, 50]), #blue
        ([35, 58, 0], [86, 255, 142]) #green
    ]
    i = 0
    for (lower, upper) in boundaries:
        # creo array lower e upper dai boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # trovo il colore all'interno dei boundaries e applico la maschera
        mask = cv2.inRange(small_frame, lower, upper)
        output = cv2.bitwise_and(small_frame, small_frame, mask=mask)
        # calcolo la ratio tra i pixel che non sono neri del frame principale e di quello a cui ho applicato la maschera
        tot_pix = count_nonblack_np(small_frame)
        color_pix = count_nonblack_np(output)
        ratio = 0
        # evito la divisione per zero
        if (tot_pix != 0):
            ratio = color_pix / tot_pix
        if i == 0:
            red_ratio = ratio
        elif i == 1:
            blue_ratio = ratio
        elif i == 2:
            green_ratio = ratio

        i += 1


    return count_distance(old_ratio,new_ratio=[red_ratio,blue_ratio,green_ratio])
