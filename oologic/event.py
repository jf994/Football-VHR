class Event:
    def __init__(self, time, type, who):
        self.time = time
        self.type = type
        self.who = who

    def json_event(self):
        event = {}
        event["time"] = self.time
        event["type"] = self.type
        event["who"] = self.who.json_person()
        return event