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
        return dataGruppenCSV, turniername, teams
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
        dataGruppenCSV.to_csv(f"turniere/{turniername}/gruppen.csv", index = False)
        return dataGruppenCSV, turniername, teams

def rundenCsvErstellen(turniername):
    rundenDict = {}
    for rundenJederGruppe in runden:
        for r in rundenJederGruppe:
            for s in r.spiele:
                rundenDict[s.paar] = s.t1.gruppe.name, s.runde, s.gespielt, s.ergebnis

    dataRundenCSV = pandas.DataFrame(rundenDict)
    dataRundenCSV.to_csv(f"turniere/{turniername}/runden.csv", index = False)
    return dataRundenCSV

def gruppenAnlage(dataGruppenCSV, turniername, teams):
    gruppenInCSV = dataGruppenCSV.gruppe.unique().tolist()
    print(f"gruppen die mitspielen: {gruppenInCSV}")

    if os.path.isfile(f"turniere/{turniername}/runden.csv"):
        dataRundenCSV = pandas.read_csv(f"turniere/{turniername}/runden.csv")
        print("es liegt ein Rundenplan vor")
        dataRunden = dataRundenCSV.to_dict()

        for g in gruppenInCSV:
            rundenWerdenGespielt = 0
            for key, value in dataRunden.items():
                paarDesSpieles   = key
                gruppeDesSpieles = value [0]
                runde            = value [1]
                gespielt         = value [2]
                ergebnis         = value [3]

                if int(runde) > rundenWerdenGespielt and gruppeDesSpieles == g:
                    rundenWerdenGespielt = int(runde)

            teamsInGruppe = []
            for tAusCSV in dataGruppenCSV[dataGruppenCSV.gruppe == g].teams.tolist():
                for t in teams:
                    if tAusCSV == t.name:
                        teamsInGruppe.append(t)
                        break
            gruppen.append(neueGruppe(g,int(rundenWerdenGespielt),teamsInGruppe))
        return gruppen

    else:
        for g in gruppenInCSV:
            teamAnz = len(dataGruppenCSV[dataGruppenCSV.gruppe == g])

            rundenWerdenGespielt = input("wie viele Runden werden gespielt? (n/e/d): ")
            if rundenWerdenGespielt[0] == "e":
                rundenWerdenGespielt = teamAnz/2*(teamAnz-1)
            else:
                if rundenWerdenGespielt[0] == "d":
                    rundenWerdenGespielt = teamAnz*(teamAnz-1)
                elif rundenWerdenGespielt > teamAnz*(teamAnz-1):
                    rundenWerdenGespielt = teamAnz*(teamAnz-1)

            print(f"es werden {int(rundenWerdenGespielt)} runden in dieser Gruppe gespielt")

            teamsInGruppe = []
            for tAusCSV in dataGruppenCSV[dataGruppenCSV.gruppe == g].teams.tolist():
                for t in teams:
                    if tAusCSV == t.name:
                        teamsInGruppe.append(t)
                        break

            gruppen.append(neueGruppe(g,int(rundenWerdenGespielt),teamsInGruppe))

        for t in teams:
            for g in gruppen:
                if t.gruppe == g.name:
                    t.gruppeAendern(g)
        return gruppen

def spielPlanErstellen(turniername, teams, gruppen):
    for g in gruppen:
        rundenAktuelleGruppe = []
        print(f"gruppe: {g.name}")
        teamsInGruppe = []
        for t in g.teamsInGruppe:
            teamsInGruppe.append(t.name)

        if len(teamsInGruppe) % 2 > 0:
            fillerTeam = "-"+str(g.name)
            teamsInGruppe.append(fillerTeam)
            teams.append(neuesTeam(fillerTeam, g))
            g.teamsAendern(team for team in teams if team.gruppe == g.name)

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
    return runden

def rundenDatenAusCSV(turniername, runden):
    if os.path.isfile(f"turniere/{turniername}/runden.csv"):
        schonGespielt = False
        dataRundenCSV = pandas.read_csv(f"turniere/{turniername}/runden.csv")
        dataRunden = dataRundenCSV.to_dict()

        for r in runden:
            for s in r.spiele:
                for key, value in dataRunden.items():
                    paarDesSpieles   = key
                    gruppeDesSpieles = value [0]
                    runde            = value [1]
                    gespielt         = value [2]
                    ergebnis         = value [3]

                    ergebnis = int(ergebnis)

                    if s.paar == paarDesSpieles and gespielt:
                        schonGespielt = True
                        s.gespielt = True
                        s.ergebnis = ergebnis
                        s.ergebnisEintragen(ergebnis[0],ergebnis[1])

        if schonGespielt:
            print("es wurden schon runden gespielt")


teams = []
gruppen = []
runden = []

def main():
    welcome()
    dataGruppenCSV, turniername, teams = turnierSetup()
    gruppen = gruppenAnlage(dataGruppenCSV, turniername, teams)
    if not os.path.isfile(f"turniere/{turniername}/runden.csv"):
        runden = spielPlanErstellen(turniername, teams, gruppen)
    else:
        runden = rundenDatenAusCSV(turniername)
    #for g in gruppen:
    #    for t in g.teamsInGruppe:
    #        print(f"team: {t.name} punkte: {t.punkte}")

if __name__ == "__main__":
    main()