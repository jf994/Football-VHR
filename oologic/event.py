class Event:
    def __init__(self, time, description, who):
        self.time = time
        self.description = description
        self.who = who

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
