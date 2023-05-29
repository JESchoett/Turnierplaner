import pandas
import os

from team import Team
from gruppe import Gruppe
from spiele import Spiel
from runde import Runde

def welcome():
    print("Willkommen beim Turnierplaner")
    if not os.path.isdir("turniere"):
        os.mkdir("turniere")

teams = []
def neuesTeam(teamName, teamGruppe):
    t = Team(name = teamName, gruppe=teamGruppe)
    return t

turniername = " "
data = " "

def turnierSetup():
    turniername = input("Turniername angeben: ")
    if os.path.isdir(f"turniere/{turniername}"):
        data = pandas.read_csv(f"turniere/{turniername}/gruppen.csv")
        print("turnier wurde gefunden")
        teamNamen = data.teams.to_list()
        teamGruppe = data.gruppe.to_list()
        for i in range(0,len(teamNamen)):
            teams.append(neuesTeam(teamNamen[i], teamGruppe[i]))
        return data
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
        return data

gruppen = []
def neueGruppe(name, spieleanzahl, teamsInGruppe):
    g = Gruppe(name, spieleanzahl, teamsInGruppe)
    return g

def gruppenAnlage(data):
    if os.path.isfile(f"turniere/{turniername}/runden.csv"):
        print("es wurden schon runden gespielt")
    else:
        gruppenInCSV = data.gruppe.unique().tolist()
        print(f"gruppen die mitspielen: {gruppenInCSV}")
        for g in gruppenInCSV:
            teamsInGruppe = len(data[data.gruppe == g])

            rundenWerdenGespielt = input("wie viele Runden werden gespielt? (n/e/d): ")
            if rundenWerdenGespielt[0] == "e":
                rundenWerdenGespielt = teamsInGruppe/2*(teamsInGruppe-1)
            elif rundenWerdenGespielt[0] == "d":
                rundenWerdenGespielt = teamsInGruppe*(teamsInGruppe-1)
            print(f"es werden {int(rundenWerdenGespielt)} runden in dieser Gruppe gespielt")
            gruppen.append(neueGruppe(g,int(rundenWerdenGespielt),data[data.gruppe == g]))

        for t in teams:
            for g in gruppen:
                if t.gruppe == g.name:
                    t.gruppeAendern(g)

runden = []
def neueRunde(nr, spiele):
    r = Runde(nr, spiele)
    return r
def neuesSpiel(paar, t1, t2):
    s = Spiel(paar, t1, t2)
    return s

def spielPlanErstellen():
    for g in gruppen:
        print("-----")
        print(f"gruppe: {g.name}")
        tInG = g.teamsInGruppe.teams.tolist()
        if len(tInG) % 2 > 0:
            tInG.append('-')
            teams.append(neuesTeam("-", g))
            g.teamsAendern(team for team in teams if team.gruppe == g)
        n = len(tInG)

        hinRundepaare = []
        rueckRundepaare = []
        for i in range(n):
            for j in range(i+1, n):
                hinRundepaare.append((tInG[i], tInG[j]))
                rueckRundepaare.append((tInG[j], tInG[i]))
        alleRunden = hinRundepaare + rueckRundepaare

        rundenAufsetzen = {}
        rundenCounter = 0
        while rundenCounter < g.spieleanzahl:
            rundenCounter += 1
            rundenPaare = []
            playedTeams = []
            for paar in alleRunden:
                team1, team2 = paar
                schonGespielt = False
                for key, value in rundenAufsetzen.items():
                    if paar in value:
                        schonGespielt = True

                if not schonGespielt and team1 not in playedTeams and team2 not in playedTeams:
                    rundenPaare.append(paar)
                    playedTeams.append(team1)
                    playedTeams.append(team2)

            rundenAufsetzen[rundenCounter] = rundenPaare

        for r in rundenAufsetzen:
            spieleInRunde = []
            for paar in rundenAufsetzen[r]:
                t1, t2 = paar
                for t in teams:
                    if t1 == t.name:
                        t1 = t
                    if t2 == t.name:
                        t2 = t
                spieleInRunde.append(neuesSpiel(paar,t1,t2))

            runden.append(neueRunde(r,spieleInRunde))

        for r in runden:
            print(f"Rundenr: {r.nr}")
            for s in r.spiele:
                print(f"es spielen: {s.paar}")
        print("-----")

def main():
    welcome()
    data = turnierSetup()
    gruppenAnlage(data)
    spielPlanErstellen()

if __name__ == "__main__":
    main()