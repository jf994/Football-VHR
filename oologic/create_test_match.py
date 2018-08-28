import csv
from oologic.person import Coach, Player, Referee
from oologic.team import Team
from oologic.match import Match


def createMatch():
    with open('oologic/match.csv', 'r') as f:
        reader = csv.reader(f)
        events = []
        n = 0
        for row in reader:
            if n == 0:
                team1 = createTeam(row[0])
                team2 = createTeam(row[1])
            else:
                referee = Referee(row[0], row[1], row[2])
            n += 1
        match = Match(team1, team2, referee, events)
    return match


def createTeam(file):
    file = 'oologic/'+str(file)
    with open(file, 'r') as f:
        reader = csv.reader(f)
        roster = []
        bench = []
        n = 0
        for row in reader:
            if n == 0:
                name = row[0]
            elif n == 1:
                coach = Coach(row[0], row[1])
            else:

                player = Player(row[0], row[1], row[2], row[3], row[4])
                if n < 13:
                    roster.append(player)
                else:
                    bench.append(player)
            n += 1
        team = Team(name, roster, bench, coach)
        return team

