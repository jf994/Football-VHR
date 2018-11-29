# nel file è presente la definizione della classe Person e delle sottoclassi derivate
# Player, Referee e Coach. Inoltre i suoi metodi permettono di tenere traccia di alcune statistiche importanti


class Person:
    def __init__(self, surname, role):
        self.surname = surname
        self.role = role

    # il metodo permette di gestire la generazione a cascata del dizionario che conterrà i dati utili alla
    # generazione automatica dei file di output
    def json_person(self):
        person = {}
        person["surname"] = self.surname
        person["role"] = self.role
        return person

    # il metodo permette di gestire autmaticamente la situazione cartellini per un giocatore all'interno del json
    # ATTENZIONE: il metodo è inutilizzato in quanto il programma non riconosce l'autore del fallo di un cartellino
    def warning(self):
        if self.y_card == 0:
            self.y_card += 1
        elif self.y_card == 1:
            self.y_card += 1
            self.expulsoin()

    def expulsion(self):
        self.r_card += 1


class Player(Person):
    def __init__(self, surname, number, role, color, is_cpt):
        super().__init__(surname, role)
        self.number = number
        self.color = color
        self.y_card = 0
        self.r_card = 0
        self.is_cpt = is_cpt

    # il metodo permette di gestire la generazione a cascata del dizionario che conterrà i dati utili alla
    # generazione automatica dei file di output
    def json_person(self):
        player = {}
        player["surname"] = self.surname
        player["number"] = self.number
        player["role"] = self.role
        player["color"] = self.color
        player["cpt"] = self.is_cpt
        if self.y_card > 0:
            player["y_card"] = self.y_card
        else:
            player["y_card"] = False
        if self.r_card == 1:
            player["r_card"] = True
        else:
            player["r_card"] = False

        return player



class Referee(Person):
    def __init__(self, surname, role, color):
        super().__init__(surname, role)
        self.color = color

    # il metodo permette di gestire la generazione a cascata del dizionario che conterrà i dati utili alla
    # generazione automatica dei file di output
    def json_person(self):
        referee = {}
        referee["surname"] = self.surname
        referee["role"] = self.role
        referee["color"] = self.color
        return referee



class Coach(Person):
    def __init__(self, surname, role):
        super().__init__(surname, role)
        self.r_card = 0

    # il metodo permette di gestire la generazione a cascata del dizionario che conterrà i dati utili alla
    # generazione automatica dei file di output
    def json_person(self):
        coach = {}
        coach["surname"] = self.surname
        coach["role"] = self.role
        if self.r_card == 1:
            coach["r_card"] = True
        return coach
