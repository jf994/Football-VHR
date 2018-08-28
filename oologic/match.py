from oologic.create_json import writeToJSONFile
from oologic.create_txt import writeToTXTFile


class Match:
    event_list = []

    def __init__(self, home_team, guest_team, referee, event_list):
        self.home_team = home_team
        self.guest_team = guest_team
        self.referee = referee
        self.event_list = event_list

    def json_and_txt_create(self):
        date = "060709"  # automatize this
        sportname = "FOOTBALL"
        leaguename = "WORLD CUP 2006"
        gamenumber = "FINAL"
        self.txt_match(date, sportname, leaguename, gamenumber)
        self.json_match(date, sportname, leaguename)

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
            if isinstance(event.who, list):
                for ppl in event.who:
                    who += str(ppl.surname) + " "
            else:
                who = str(event.who.surname)

            printingstring += "    "+str(time)+'     '+str(label)+'     '+str(who)+'\n'
        writeToTXTFile('txt', str(self.home_team.name)+" VS "+str(self.guest_team.name), printingstring)