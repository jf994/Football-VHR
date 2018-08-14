class Person:
    def __init__(self, surname, role):
        self.surname = surname
        self.role = role


class Player(Person):
    def __init__(self, surname, number, role, color):
        super().__init__(surname, role)
        self.number = number
        self.color = color

    def json_person(self):
        player = {}
        player["surname"] = self.surname
        player["number"] = self.number
        player["role"] = self.role
        player["color"] = self.color
        return player



class Referee(Person):
    def __init__(self, surname, role, color):
        super().__init__(surname, role)
        self.color = color

    def json_person(self):
        referee = {}
        referee["surname"] = self.surname
        referee["role"] = self.role
        referee["color"] = self.color
        return referee



class Coach(Person):
    def __init__(self, surname, role):
        super().__init__(surname, role)

    def json_person(self):
        coach = {}
        coach["surname"] = self.surname
        coach["role"] = self.role
        return coach
