
class Team:

    def __init__(self, name, roster, banch, coach):
        self.name = name
        self.roster = roster
        self.banch = banch
        self.coach = coach
        self.score = 0

    def score_goal(self):
        self.score += 1
        return self.score

    def json_team(self):
        team = {}
        team["name"] = self.name
        team["roster"] = []
        for player in self.roster:
            team["roster"].append(player.json_person())

        team["banch"] = []
        for player in self.banch:
            team["banch"].append(player.json_person())

        team["coach"] = self.coach.json_person()
        return team
