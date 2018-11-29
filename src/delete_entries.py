# nel file è presente la funzione che permette di cancellare gli eventi
# tra un tempo e l'altro dovuti agli spot pubblicitari


# la funzione controlla, per ogni evento che la sua descrizione inizi con le parole chiave 'Start' o 'End'
# myList è la lista degli eventi del match ordinata per tempo di occorrenza, tutti gli eventi tra un 'End' e un 'Start'
# devono essere eliminati in quanto falsi positivi, tali eventi non vengono aggiunti alla lista di passaggio che poi
# viene ritornata dalla funzione e risulta cosi pulita
def delete_false_positive(mylist):
    new_list = []
    delete = False
    for ev in mylist:

        if 'Start ' in ev.description:
            delete = False

        if not delete:
            new_list.append(ev)

        if 'End ' in ev.description:
            delete = True

    return new_list
