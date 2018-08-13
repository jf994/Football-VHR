class Match:
    event_list = []

    def __init__(self, home_team, guest_team, referee, event_list):
        self.home_team = home_team
        self.guest_team = guest_team
        self.referee = referee
        self.event_list = event_list

    def generaJson(self):
        date4string = "060709"  # automatize this
        title = "FOOTBALL WORLD CUP 2006 "+str(self.home_team.name)+" VS "+str(self.guest_team.name)+\
                "   "+str(date4string)
        subtitle = "FOOTBALL WORLD CUP 2006 FINAL "+str(self.home_team.name) + \
                   " VS "+str(self.guest_team.name)+" "+str(self.home_team.score)+"-"+str(self.guest_team.score)
        printingString = title+"\n"+subtitle+"\n"
        for event in self.event_list:
            time = str(event.time)
            label = str(event.type)
            who = str(event.who)

            data = "    "+str(time)+'     '+str(label)+'     '+str(who)+'\n'

            #writeToJSONFile('json', str(label)), data)
            printingString += data
        print(printingString)
