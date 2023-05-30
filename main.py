import pandas
import os
import random

from team import Team
from gruppe import Gruppe
from spiele import Spiel
from runde import Runde

def welcome():
    print("Willkommen beim Turnierplaner")
    if not os.path.isdir("turniere"):
        os.mkdir("turniere")

teams = []
gruppen = []
runden = []

def neuesTeam(teamName, teamGruppe):
    t = Team(name = teamName, gruppe=teamGruppe)
    return t
def neueGruppe(name, spieleanzahl, teamsInGruppe):
    g = Gruppe(name, spieleanzahl, teamsInGruppe)
    return g
def neueRunde(nr, spiele):
    r = Runde(nr, spiele)
    return r
def neuesSpiel(paar, t1, t2, nr):
    s = Spiel(paar, t1, t2, nr)
    return s

def turnierSetup():
    turniername = input("Turniername angeben: ")
    if os.path.isdir(f"turniere/{turniername}"):
        dataGruppenCSV = pandas.read_csv(f"turniere/{turniername}/gruppen.csv")
        print("turnier wurde gefunden")
        teamNamen = dataGruppenCSV.teams.to_list()
        teamGruppe = dataGruppenCSV.gruppe.to_list()
        for i in range(0,len(teamNamen)):
            teams.append(neuesTeam(teamNamen[i], teamGruppe[i]))
        return dataGruppenCSV, turniername
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
        dataGruppenCSV = pandas.DataFrame(teamsDict)
        dataGruppenCSV.to_csv(f"turniere/{turniername}/gruppen.csv")
        return dataGruppenCSV

def rundenCsvErstellen(turniername):
    rundenDict = {}
    for gruppen in runden:
        for r in gruppen:
            for s in r.spiele:
                rundenDict[s.paar] = s.t1.gruppe.name, s.t1.name, s.t2.name, s.runde, s.gespielt

    dataRundenCSV = pandas.DataFrame(rundenDict)
    dataRundenCSV.to_csv(f"turniere/{turniername}/runden.csv")
    return dataRundenCSV

def spielPlanErstellen(turniername):
    for g in gruppen:
        rundenAktuelleGruppe = []
        print(f"gruppe: {g.name}")
        teamsInGruppe = g.teamsInGruppe.teams.tolist()
        if len(teamsInGruppe) % 2 > 0:
            teamsInGruppe.append('-')
            teams.append(neuesTeam("-", g))
            g.teamsAendern(team for team in teams if team.gruppe == g)

        random.shuffle(teamsInGruppe)

        hinRundepaare = []
        rueckRundepaare = []
        for i in range(len(teamsInGruppe)):
            for j in range(i+1, len(teamsInGruppe)):
                hinRundepaare.append((teamsInGruppe[i], teamsInGruppe[j]))
                rueckRundepaare.append((teamsInGruppe[j], teamsInGruppe[i]))
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

        rundenCounter = 0
        for r in rundenAufsetzen:
            rundenCounter += 1
            spieleInRunde = []
            for paar in rundenAufsetzen[r]:
                t1, t2 = paar
                for t in teams:
                    if t1 == t.name:
                        t1 = t
                    if t2 == t.name:
                        t2 = t
                paar = (f"{t1.name}/{t2.name}")
                spieleInRunde.append(neuesSpiel(paar,t1,t2,rundenCounter))

            rundenAktuelleGruppe.append(neueRunde(r,spieleInRunde))

        runden.append(rundenAktuelleGruppe)

        for r in rundenAktuelleGruppe:
            print(f"Rundenr: {r.nr}")
            for s in r.spiele:
                print(f"es spielen: {s.paar}")
        print("-----")
    rundenCsvErstellen(turniername)
    return runden

def gruppenAnlage(dataGruppenCSV, turniername):
    gruppenInCSV = dataGruppenCSV.gruppe.unique().tolist()
    print(f"gruppen die mitspielen: {gruppenInCSV}")

    if os.path.isfile(f"turniere/{turniername}/runden.csv"):
        dataRundenCSV = pandas.read_csv(f"turniere/{turniername}/runden.csv")
        print("es wurden schon runden gespielt")
        #for g in gruppenInCSV:
        #gruppen.append(neueGruppe(g,int(max Rundenanzahl),dataGruppenCSV[dataGruppenCSV.gruppe == g]))
    else:
        for g in gruppenInCSV:
            teamsInGruppe = len(dataGruppenCSV[dataGruppenCSV.gruppe == g])

            rundenWerdenGespielt = input("wie viele Runden werden gespielt? (n/e/d): ")
            if rundenWerdenGespielt[0] == "e":
                rundenWerdenGespielt = teamsInGruppe/2*(teamsInGruppe-1)
            else:
                if rundenWerdenGespielt[0] == "d":
                    rundenWerdenGespielt = teamsInGruppe*(teamsInGruppe-1)
                elif rundenWerdenGespielt > teamsInGruppe*(teamsInGruppe-1):
                    rundenWerdenGespielt = teamsInGruppe*(teamsInGruppe-1)

            print(f"es werden {int(rundenWerdenGespielt)} runden in dieser Gruppe gespielt")
            gruppen.append(neueGruppe(g,int(rundenWerdenGespielt),dataGruppenCSV[dataGruppenCSV.gruppe == g]))

        for t in teams:
            for g in gruppen:
                if t.gruppe == g.name:
                    t.gruppeAendern(g)
        spielPlanErstellen(turniername)

def main():
    welcome()
    dataGruppenCSV, turniername = turnierSetup()
    runden = gruppenAnlage(dataGruppenCSV, turniername)

if __name__ == "__main__":
    main()