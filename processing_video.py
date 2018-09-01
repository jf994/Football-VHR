# nel file è presente la funzione principale del programma che gestisce la letura e le analisi sul video

import cv2
from darkflow.net.build import TFNet
import time
import datetime
from oologic.event import Event
from get_color import detect_color
from get_scene_change import is_new_scene,count_distance
from face_rec import get_faces, get_names_from_image
from oologic.create_test_match import createMatch
from oologic.person import Person
from get_options import get_opt
from count_white_pixels import count_difference_white
from collections import Counter
from get_crops import get_crops
from delete_entries import delete_false_positive


# la funzione si occupa di assegnare i primi 3 elementi del vettore temp ai primi 3 di vector
def assign_vector(vector, vector_temp):
        for i in range(0, 3):
            vector[i] = vector_temp[i]

# la funzione cerca nelle liste del match e contenute in where e appende alla lista who_list l'oggetto Player relativo al
# nome presente nella stringa who
def look_for(who, where, who_list):
    for mlist in where:
        for el in mlist:
            if el.surname == who:
                who_list.append(el)


temp_opt = get_opt()  # la chiamata a funzione raccoglie i valori per option
crop_array = get_crops()  # ottengo le zone dei crops
match = createMatch()  # creo l'oggetto match

option = {
    'model': 'cfg/tiny-yolo-voc-2c.cfg',
    'load': int(temp_opt[2]),
    'threshold': float(temp_opt[1]),
    'gpu': 1.0
}


frame_rate_originale = int(temp_opt[3])
capture = cv2.VideoCapture(str(temp_opt[0]))
height = round(capture.get(4))  # altezza del frame (usata per settare la posizione del valore degli FPS)
tfnet = TFNet(option)

# variabili golbali
last_tag_time = 0  # contiene il time dell'ultimo cartellino
num_frame_scena = 0  # contiene il numero del frame in cui è stato registrato l'ultimo cambio di scena
current_frame_scena = 0  # contiene il numero del frame in cui è stato registrato il cambio per la scena attuale
num_frame = 0  # contiene il numero di frame processati
temp_num_frame = 1  # è incrementato sino al frame rate del video per calcolare i tempi in secondi
count = 0  # contatore che controlla che la scena sia cambiata per considerare il tabellone come apparso
count_event = 0  # contatore che controlla che un evento perduri nel tempo per considerarlo valido
count_tabellone_on = 0  # contatore che verifica il riapparire del tabellone per la conferma di un evento
are_even = 0  # esprime la differenza reti attuale 0- pari pos- vantaggio ospiti neg- vantaggio casa
crop_old_home = 0  # contiene il frame tagliato con lo score della squadra di casa per comparazione successiva
crop_old_guest = 0  # contiene il frame tagliato con lo score della squadra ospite per comparazione successiva
half_time = 0  # conta le meta di tempo passate supplementari inclusi
THRESHOLD = 5  # costante contenente il numero di volte in cui una faccia deve comparire in una scena per essere rilevata
saw_card = 0  # variabile che aumenta a ogni cartellino valido superato 5 considera l'evento avvenuto
start_time = datetime.datetime.now()  # contiene l'oggetto datetime di comparsa del cartellone per calcolo del tempo
temp_scene = [0, 0, 0, 0]  # contiene valori temporanei relativi alle ratio e alle loro variazioni tra le scene
old_ratio = [0, 0, 0]  # contiene le ratio dell'ultima scena salvata per comparazione successiva
tabellone_ratios = [0, 0, 0]  # contiene le ratio del tabellone per controllare la sua ricomparsa
temp_ratios_topleft = [0, 0, 0]  # attuali ration nella zona del tabellone per comparazione successiva
face_in_scene = []  # tiene traccia delle stringhe delle persone trovate dall'algoritmo di face recognition in una scena


unknown_person = Person('Unknown', '')  # dichiarazione di un oggetto persona Unknown per consistenza

event_on = False  # flag utile a ricordare che un evento è stato riconosciuto
tabellone_on = False  # flag utile a ricordare che il tabellone è stato riconosciuto
end_half = False  # flag utile a ricordare che un tempo di gioco si è concluso

# variabili per la logica json
who_list = []  # lista contenente le persone da cercare
where_list = []  # lista contenete i luoghi dove cercare le persone
others = []  # lista di supporto per salvare coach e referee

# creazione di where list
where_list.append(match.home_team.roster)
where_list.append(match.guest_team.roster)
where_list.append(match.home_team.bench)
where_list.append(match.guest_team.bench)

others.append(match.home_team.coach)
others.append(match.guest_team.coach)
others.append(match.referee)
where_list.append(others)

# funzioni che preparano il programma per la face recognition
get_names_from_image(match.home_team.name)
get_names_from_image(match.guest_team.name)
get_names_from_image("Ref")

print("Done.")


# inizio loop principale per analisi video che continua sino a che il video non finisce o viene forzatamente interrotto
while(capture.isOpened()):
    stime = time.time()  # variabile utile al calcolo degli fps
    sicurezza = 0  # indica la confidece con cui è stato riconosciuto un cartellino
    ret, frame = capture.read()

    if ret:
        # controllo le facce ogni 3 frame
        if(temp_num_frame % 3 == 0):
            frame = get_faces(frame, face_in_scene)
        # ogni 2 secondi controllo la scena e il risultato
        if(temp_num_frame == (frame_rate_originale * 2)):
            # calcolo ratio e variazione valori RGB per controllare cambio scena
            temp_scene = is_new_scene(frame, old_ratio, True)
            assign_vector(old_ratio, temp_scene)
            temp_num_frame = 1
            # verifico l'avvenuto cambio di scena...
            if(temp_scene[3] > .1):
                # ...se la scena è cambiata...
                saw_card = 0
                num_frame_scena = num_frame
                counter = Counter(face_in_scene)
                players = Counter(el for el in counter.elements() if counter[el] >= THRESHOLD).keys()
                # ...controllo che almeno un giocatore sia stato riconoscito un numero di volte maggiore del threshold
                if players.__len__() > 0:
                    for player in players:
                        # per ognuno dei player trovati ricerco il suo oggetto player e creo l'evento
                        look_for(player, where_list, who_list)
                    event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale)))),
                                  "Close-up of ",
                                  who_list)
                    match.event_list.append(event)
                # infine azzero entrambe le liste
                who_list = []
                face_in_scene = []

            # ritaglio il frame dove dovrebbe essere il tabellone col risultato
            crop = frame[int(crop_array[0][0]):int(crop_array[0][1]), int(crop_array[0][2]):int(crop_array[0][3])]
            temp_topleft = is_new_scene(crop, temp_ratios_topleft, False)
            assign_vector(temp_ratios_topleft, temp_topleft)
            # se il tabellone è già stato trovato...
            if (tabellone_on):
                # ...verifico se sia ancora presente o meno...
                distance = count_distance(tabellone_ratios, temp_ratios_topleft)[3]
                temp_ratios_topleft.pop()
                # ...se è assente...
                if (distance>0.03):
                    # ...conto
                    count_event += 1
                    # ...arrivati a 12 secondi di assenza (6 * 2 volte il frame rate)...
                    if (count_event == 6):
                        #confermo l'avvenuto evento
                        event_on = True
                        count_tabellone_on = 0
                        current_frame_scena = num_frame_scena

                    # dopo 2 minuti di assenza del tabellone, assumiamo la fine del tempo
                    elif (count_event == 60 and not end_half):
                        string = ''
                        end_half = True
                        half_time += 1
                        # controllo che tempo è stato raggiunto e salvo l'evento relativo insieme al risultato parziale
                        if (half_time == 1):
                            string = 'End first half: '+str(match.home_team.name)+" "+str(match.home_team.score)+"-"\
                                     + str(match.guest_team.score)+" "+str(match.guest_team.name)
                        elif (half_time == 2):
                            string = 'End second half: '+str(match.home_team.name)+" "+str(match.home_team.score)+"-"\
                                     + str(match.guest_team.score)+" "+str(match.guest_team.name)
                        elif (half_time == 3):
                            string = 'End extra time first half: '+str(match.home_team.name)+" "+str(match.home_team.score)+"-"\
                                     + str(match.guest_team.score)+" "+str(match.guest_team.name)
                        elif (half_time == 4):
                            string = 'End extra time second half: '+str(match.home_team.name)+" "+str(match.home_team.score)+"-"\
                                     + str(match.guest_team.score)+" "+str(match.guest_team.name)

                        event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                           (count_event * 2)))),
                                      string,
                                      unknown_person)
                        match.event_list.append(event)
                # ...se è presente per almeno 4 secondi e la scena generale è cambiata...
                elif(distance <= 0.03 and count_tabellone_on == 2 and num_frame_scena !=  current_frame_scena):
                    # ...nel caso si fosse verificato un evento fine tempo...
                    if(end_half):
                        # ...gestisco l'evento di ripresa di tempo di gioco
                        end_half = False
                        event_on = False
                        string = ''
                        if (half_time == 1):
                            string = 'Start second half'
                        elif (half_time == 2):
                            string = 'Start extra time first half'
                        elif (half_time == 3):
                            string = 'Start extra time second half'
                        event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) - 5))),
                                      string,
                                      unknown_person)
                        match.event_list.append(event)

                    # ...altrimenti è riapparso il tabellone, controllo che tipo di evento è avvenuto...
                    if(event_on):
                        # ...taglio i crop dei punteggi e indago il tipo di evento verificatosi
                        event_on = False
                        crop_h = frame[crop_array[1][0]:crop_array[1][1], crop_array[1][2]:crop_array[1][3]]
                        crop_g = frame[crop_array[2][0]:crop_array[2][1], crop_array[2][2]:crop_array[2][3]]
                        diff_crop = count_difference_white(crop_h, crop_g, crop_old_home, crop_old_guest)
                        # se è avvenuto un evento Goal Home...
                        if(are_even <= 0 and diff_crop == -1) \
                                or (are_even == 1 and diff_crop == 0) \
                                or (are_even > 1 and diff_crop == -1):

                            are_even -= 1  # are even viene decrementato
                            match.home_team.score_goal()  # registro il goal nell'oggetto match
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count_event * 2) - 25))),
                                          'Goal '+str(match.home_team.name),
                                          unknown_person)  # salvo l'evento
                            match.event_list.append(event)
                            # memorizzo i nuovi crop del tabellone cambiato, e del punteggio di casa
                            crop_old_home = frame[crop_array[1][0]:crop_array[1][1], crop_array[1][2]:crop_array[1][3]]
                            crop = frame[crop_array[0][0]:crop_array[0][1], crop_array[0][2]:crop_array[0][3]]
                            # calcolo della nuova ratio
                            temp_topleft = is_new_scene(crop, temp_ratios_topleft, False)
                            assign_vector(tabellone_ratios, temp_topleft)
                        # se è avvenuto un evento Goal Guest...
                        elif(are_even >= 0 and diff_crop == 1) \
                                or (are_even == -1 and diff_crop == 0) \
                                or (are_even < -1 and diff_crop == 1):
                            are_even += 1  # are even viene incrementato
                            match.guest_team.score_goal()  # registro il goal nell'oggetto match
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count_event * 2) - 25))),
                                           'Goal '+str(match.guest_team.name),
                                           unknown_person)  # salvo l'evento
                            match.event_list.append(event)
                            # memorizzo i nuovi crop del tabellone cambiato, e del punteggio degli ospiti
                            crop_old_guest = frame[crop_array[2][0]:crop_array[2][1], crop_array[2][2]:crop_array[2][3]]
                            crop = frame[crop_array[0][0]:crop_array[0][1], crop_array[0][2]:crop_array[0][3]]
                            # calcolo della nuova ratio
                            temp_topleft = is_new_scene(crop, temp_ratios_topleft, False)
                            assign_vector(tabellone_ratios, temp_topleft)

                        else:
                            #altrimenti evento minispot
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count_event * 2) - 4))),
                                           'Mini spot',
                                           unknown_person)
                            match.event_list.append(event)
                    count_event = 0
                # se il tabellone è presente e non ha ancora contato sino a due...
                elif(distance <= 0.03 and count_tabellone_on != 2):
                    # solo nel caso in cui la scena sia cambiata
                    if(num_frame_scena !=  current_frame_scena):
                        count_tabellone_on += 1 # incremento il count del tabellone

            # se il tabellone non è ancora stato trovato...
            else:
                # ...nel caso in cui si rilevi una variazione minima...
                if(temp_topleft[3] > 0 and temp_topleft[3] < .02):
                    # ...inizio a contare e, nel caso sia il primo giro, salvo la scena attuale
                    if(count == 0):
                        current_frame_scena = num_frame_scena
                    count += 1
                    # dopo 10 secondi senza variazioni significative...
                    if(count == 5):
                        # controllo che ci sia stato almeno un cambio di scena
                        if(num_frame_scena !=  current_frame_scena):
                            start_time = datetime.datetime.now()
                            # confermo la presenza del cartellone e salvo nuovi crop e ratio
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count * 2)))),
                                          'Start first half',
                                          unknown_person)
                            match.event_list.append(event)

                            crop_old_home = frame[crop_array[1][0]:crop_array[1][1], crop_array[1][2]:crop_array[1][3]]
                            crop_old_guest = frame[crop_array[2][0]:crop_array[2][1], crop_array[2][2]:crop_array[2][3]]
                            assign_vector(tabellone_ratios, temp_ratios_topleft)
                            tabellone_on = True
                        else:
                            # se la scena non è cambiata, decremento count e ricontrollo
                            count -= 1
                else:
                    # se ho ottenuto una variazione eccessiva, azzero count
                    count = 0

        # controllo che la rete neurale dei cartellini abbia trovato risultati nel frame
        results = tfnet.return_predict(frame)
        # scorro tali risultati
        for result in results:
            # ricavo label, confidence e posizione del risultato positivo
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            confidence = result['confidence']
            sicurezza = confidence
            text = '{}: {:.0f}%'.format(label,confidence * 100)

            # ritaglio il bounding box da analizzare
            ymin = int(result['topleft']['y'])
            xmin = int(result['topleft']['x'])
            ymax = int(result['bottomright']['y'])
            xmax = int(result['bottomright']['x'])

            # ritaglio il frame per il controllo del colore
            crop_img = frame[ymin:ymax, xmin:xmax]
            color = detect_color(crop_img)

            # dopo aver controllato il colore predominante lo confronto con la label e
            # abbasso la sicurezza in caso di risultati incerto o discordante
            # se il colore è discordante, elimino il risultato trovato, altrimenti, se non è sicuro,
            # mantengo il risultato solo se questo è >= del 98% di sicurezza
            if "card" in str(label):
                if label == 'red_card':
                    if color == 'not_sure':
                        sicurezza -= .42
                    elif color == 'yellow':
                        sicurezza -= .50
                elif label == 'yellow_card':
                    if color == 'not_sure':
                        sicurezza -= .42
                    elif color == 'red':
                        sicurezza -= .50
            # se la sicurezza è maggiore del treshold dopo questi controlli...
            if sicurezza > option['threshold']:
                # ...incremento saw card
                saw_card += 1
                if (saw_card > 4):
                    # se saw card ha superato 4 l'evento cartellino è confermato e disegno i bounding boxes
                    frame = cv2.rectangle(frame, tl, br, (255, 255, 255), 5)
                    frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)



        # calcolo degli fps
        fps = 1 / (time.time() - stime)
        num_frame += 1
        temp_num_frame += 1
        frame = cv2.putText(frame, 'FPS {:.1f}'.format(fps), (5, height-10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('frame', frame)  # dopo aver modificato il frame nell'analisi, lo mostro a video
        # se sono passati almeno 5 secondi dall'utlimo cartellino salvato...
        if (time.time() - last_tag_time) > 5:
            # ...se la sicurezza è maggiore del threshold stabilito e ho contato sino a 5...
            if sicurezza > option['threshold'] and saw_card == 5:
                # ... salvo l'evento corrispondente
                last_tag_time = time.time()

                if (label == 'yellow_card'):
                    label = 'Yellow card'
                elif (label == 'red_card'):
                    label = 'Red card'

                event = Event(str(datetime.timedelta(seconds=round(num_frame / frame_rate_originale))), label, unknown_person)
                match.event_list.append(event)
        # controllo per la chiusura prematura del ciclo
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # gestisco la creazione degli output json e txt
    else:
        # ordino gli eventi cronologicamente nella lista
        match.event_list.sort(key=lambda r: datetime.datetime.strptime(r.time, "%H:%M:%S"))
        # elimino gli eventi falsi positivi dovuti agli spot
        match.event_list = delete_false_positive(match.event_list)
        mformat = "%H:%M:%S"
        # miglioro la visualizzazione dei tempi utilizzando come tempo 0 l'ora di comparsa del tabellone
        for ev in match.event_list:
            event_time = time.strptime(ev.time, mformat)
            event_time = datetime.timedelta(seconds=round(datetime.timedelta(hours=event_time.tm_hour,
                                                                             minutes=event_time.tm_min,
                                                                             seconds=event_time.tm_sec)
                                                          .total_seconds()))
            event_time += start_time
            ev.time = str(event_time).split('.')[0].split(' ')[1]

        # chiamo la funzione che genera gli output e la distruzione delle finestre
        match.json_and_txt_create()
        capture.release()
        cv2.destroyAllWindows()
        break
