# il file permette il riconoscimento dell'avvenuto cambiamento (o meno) del risultato della partita

import numpy as np
import cv2

# la funzione analizza il risultato della partita
def count_difference_white(home, guest, old_home, old_guest):
    # numero pixel bianchi per i punteggi delle due squadre
    white_pixels_home = 0
    white_pixels_guest = 0

    # porto i frame ritagliati dei punteggi in scala di grigio
    gray_home = cv2.cvtColor(home, cv2.COLOR_BGR2GRAY)
    gray_guest = cv2.cvtColor(guest, cv2.COLOR_BGR2GRAY)

    # conto il numero dei pixel che superano un certo valore (cerco il bianco del punteggio)
    white_pixels_home += np.count_nonzero(gray_home > 190)
    white_pixels_guest += np.count_nonzero(gray_guest > 190)
    # calcolo la differenza tra il risultato delle due squadre...
    difference = white_pixels_home - white_pixels_guest

    # ...se la differenza supera un certo threshold...
    if (difference < -10 or difference > 10):
        # porto i frame ritagliati dei vecchi punteggi in scala di grigio
        gray_home_old = cv2.cvtColor(old_home, cv2.COLOR_BGR2GRAY)
        gray_guest_old = cv2.cvtColor(old_guest, cv2.COLOR_BGR2GRAY)

        # conto il numero dei pixel dei vecchi punteggi che superano un certo valore (cerco il bianco)
        white_pixels_home_old = np.count_nonzero(gray_home_old > 190)
        white_pixels_guest_old = np.count_nonzero(gray_guest_old > 190)

        # calcolo la differenza tra il nuovo punteggio di una squadra e quello vecchio (vedo se è variato)
        difference_h = white_pixels_home - white_pixels_home_old
        difference_g = white_pixels_guest - white_pixels_guest_old

        # se la squadra di casa ha variato il suo punteggio ritorno -1 (ha segnato)
        if (difference_h < -10 or difference_h > 10):
            return -1
        # se la squadra ospite ha variato il suo punteggio ritorno 1 (ha segnato)
        elif(difference_g < -10 or difference_g > 10):
            return 1

    # altrimenti ritorno zero
    return 0
