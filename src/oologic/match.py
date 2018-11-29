# nel file è presente la definizione della classe Match che gestisce la struttura della partita e i suoi metodi

from oologic.create_json import writeToJSONFile
from oologic.create_txt import writeToTXTFile
import csv



class Match:
    event_list = []

    def __init__(self, home_team, guest_team, referee, event_list):
        self.home_team = home_team
        self.guest_team = guest_team
        self.referee = referee
        self.event_list = event_list

    # il metodo legge da un file csv alcune informazioni generiche sulla partita e chiama le due funzioni che permettono
    # la creazione a cascata dei vari dizionari per la compilazione finale del json di output
    def json_and_txt_create(self):
        with open('oologic/template.csv', 'r') as f:
            reader = csv.reader(f)
            template = list(reader)[0]
            date = template[0]
            sportname = template[1]
            leaguename = template[2]
            gamenumber = template[3]
        self.txt_match(date, sportname, leaguename, gamenumber)
        self.json_match(date, sportname, leaguename)

    # il metodo imposta l'effettiva creazione dei vari dizionari json chiamando infine la funzione per la scrittura
    # dell'output
    def json_match(self, date, sportname, leaguename):
        match = {}

        match["sport"] = str(sportname)
        match["league"] = str(leaguename)
        match["date"] = str(date)
        match["home team"] = self.home_team.json_team()
        match["guest team"] = self.guest_team.json_team()

        match["event list"] = []
        for event in self.event_list:
            match["event list"].append(event.json_event())
        writeToJSONFile('json', str(self.home_team.name)+" VS "+str(self.guest_team.name), match)

    # il metodo imposta l'effettiva creazione di una stringa la quale verrà stampata nel file txt di output
    def txt_match(self, date, sportname, leaguename, gamenumber):
        printingstring = ""
        title = str(sportname) + " " + str(leaguename) + " " + str(self.home_team.name) + " VS " + str(
            self.guest_team.name) + \
                "   " + str(date)
        subtitle = str(sportname) + " " + str(leaguename) + " " + str(gamenumber) + " " + str(self.home_team.name) + \
                   " VS " + str(self.guest_team.name) + " " + str(self.home_team.score) + "-" + str(
            self.guest_team.score)
        printingstring = title + "\n" + subtitle + "\n"

        for event in self.event_list:
            time = str(event.time)
            self.str = str(event.description)
            label = self.str

            who = ""
            if isinstance(event.who, list):  # talvolta who è un giocatore, talvolta è una lista
                for ppl in event.who:
                    who += str(ppl.surname) + " "
            else:
                who = str(event.who.surname)

            printingstring += "    "+str(time)+'     '+str(label)+'     '+str(who)+'\n'
        writeToTXTFile('txt', str(self.home_team.name)+" VS "+str(self.guest_team.name), printingstring)