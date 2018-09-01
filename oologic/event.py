# nel file è presente la definizione della classe Event che gestisce un qualsiasi evento e i suoi metodi


class Event:
    def __init__(self, time, description, who):
        self.time = time
        self.description = description
        self.who = who

    # il metodo permette di gestire la generazione a cascata del dizionario che conterrà i dati utili alla
    # generazione automatica dei file di output
    def json_event(self):
        event = {}
        event["time"] = self.time
        event["description"] = self.description
        event["who"] = []
        if isinstance(self.who, list):
            for player in self.who:
                event["who"].append(player.json_person())
        else:
            event["who"].append(self.who.json_person())
        return event
