import pandas
import os

from team import Team
from gruppe import Gruppe
from runde import Runde

teams = []
def neuesTeam(teamName, teamGruppe):
    t = Team(name = teamName, gruppe=teamGruppe)
    return t

print("Willkommen beim Turnierplaner")

if not os.path.isdir("turniere"):
    os.mkdir("turniere")

turniername = input("Turniername angeben: ")

if os.path.isdir(f"turniere/{turniername}"):
    data = pandas.read_csv(f"turniere/{turniername}/gruppen.csv")
    print("turnier wurde gefunden")
    teamNamen = data.teams.to_list()
    teamGruppe = data.gruppe.to_list()
    for i in range(0,len(teamNamen)):
        teams.append(neuesTeam(teamNamen[i], teamGruppe[i]))
else:
    print("kein turnier gefunden... ein neues turnier wird angelegt")
    os.mkdir(f"turniere/{turniername}")

    teamAnlegen = True
    while teamAnlegen:
        weitereAnlage = input("möchtest du ein neues Team Anlegen? (J/N): ")
        if  weitereAnlage == "N" or weitereAnlage == "n":
            teamAnlegen = False
        else:
            teamName = input("Team Name angeben: ")
            teamGruppe = input("in welcher Gruppe soll das Team Spielen?: ")
            if len(teamGruppe) == 0:
                teamGruppe = 0
            teams.append(neuesTeam(teamName, teamGruppe))

    teamsDict = {
        "teams": [t.name for t in teams],
        "gruppe": [t.gruppe for t in teams]
    }
    data = pandas.DataFrame(teamsDict)
    data.to_csv(f"turniere/{turniername}/gruppen.csv")


rundenWerdenGespielt = 0
rundenGespielt = 0

gruppen = []
def neueGruppe(name, spieleanzahl, teamsInGruppe):
    g = Gruppe(name, spieleanzahl, teamsInGruppe)
    return g
ruden = []
def neueRunde(nr, teamsDieSpielen):
    r = Runde(nr, teamsDieSpielen)
    return r


if os.path.isfile(f"turniere/{turniername}/runden.csv"):
    print("es wurden schon runden gespielt")
else:
    gruppenInCSV = data.gruppe.unique().tolist()
    print(f"gruppen die mitspielen: {gruppenInCSV}")
    for g in gruppenInCSV:
        print(f"gruppe: {g}")
        teamsInGruppe = len(data[data.gruppe == g])

        rundenWerdenGespielt = input("wie viele Runden werden gespielt? (n/e/d): ")
        if rundenWerdenGespielt[0] == "e":
            rundenWerdenGespielt = teamsInGruppe/2*(teamsInGruppe-1)
        elif rundenWerdenGespielt[0] == "d":
            rundenWerdenGespielt = teamsInGruppe*(teamsInGruppe-1)
        print(f"es werden {int(rundenWerdenGespielt)} runden in dieser Gruppe gespielt")
        gruppen.append(neueGruppe(g,int(rundenWerdenGespielt),data[data.gruppe == g]))

for g in gruppen:
    tInG = g.teamsInGruppe.teams.tolist()
    if len(tInG) % 2 > 0:
        tInG.append('-')
    n = len(tInG)
    teams.append(neuesTeam("-", g.name))

    hinRundepaare = []
    rueckRundepaare = []
    for i in range(n):
        for j in range(i+1, n):
            hinRundepaare.append((tInG[i], tInG[j]))
            rueckRundepaare.append((tInG[j], tInG[i]))
    alleRunden = hinRundepaare + rueckRundepaare

    #roundPairings = []
    #playedTeams = []
    #for runde in range(0,g.spieleanzahl):

    #    for pairing in alleRunden:
    #        team1, team2 = pairing
    #        if team1 not in playedTeams and team2 not in playedTeams:
    #            roundPairings.append(pairing)
    #            playedTeams.append((team1, team2))
    #    print(roundPairings)
