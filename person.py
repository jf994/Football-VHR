class Person:
    def __init__(self, surname, role):
        self.surname = surname
        self.role = role


class Player(Person):
    def __init__(self, surname, number, role, color):
        super().__init__(surname, role)
        self.number = number
        self.color = color


class Referee(Person):
    def __init__(self, surname, role, color):
        super().__init__(surname, role)
        self.color = color


class Coach(Person):
    def __init__(self, surname, role):
        super().__init__(surname, role)
