
class Team:

    def __init__(self, name, roster, bench, coach):
        self.name = name
        self.roster = roster
        self.bench = bench
        self.coach = coach
        self.score = 0

    def score_goal(self):
        self.score += 1
        return self.score

    def substitution(self, player1, player2):
        for p1 in self.roster:
            if p1 == player1:
                temp1 = p1
                for p2 in self.bench:
                    if p2 == player2:
                        temp2 = p2
                        self.roster.remove(player1)
                        self.bench.remove(player2)
                        self.roster.append(temp2)
                        self.bench.append(temp1)


    def json_team(self):
        team = {}
        team["name"] = self.name
        team["roster"] = []
        for player in self.roster:
            team["roster"].append(player.json_person())

        team["bench"] = []
        for player in self.bench:
            team["bench"].append(player.json_person())

        team["coach"] = self.coach.json_person()
        return team
