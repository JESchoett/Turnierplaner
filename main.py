"""
Ablaufsteuerung des Turnierplans
"""

import os
import random
import pandas

from team import Team
from gruppe import Gruppe
from spiele import Spiel
from runde import Runde

def welcome():
    """
    Willkommensnachricht und erstellung des Ordners turniere,
    sollte dieser nicht existieren
    """
    print("Willkommen beim Turnierplaner")
    if not os.path.isdir("turniere"):
        os.mkdir("turniere")


def neues_team(name_des_teams, gruppe_des_teams):
    """
    anlage eines Team Objektes
    """
    erstelltes_team = Team(name = name_des_teams, gruppe=gruppe_des_teams)
    return erstelltes_team

def neue_gruppe(name, spieleanzahl, teams_in_gruppe):
    """
    anlage eines Gruppe Objektes
    """
    erstellte_gruppe = Gruppe(name, spieleanzahl, teams_in_gruppe)
    return erstellte_gruppe

def neue_runde(rundenzahl, spiele):
    """
    anlage eines Runde Objektes
    """
    erstellte_runde = Runde(rundenzahl, spiele)
    return erstellte_runde

def neues_spiel(paar, team_1, team_2, runde, gespielt):
    """
    anlage eines Spiel Objektes
    """
    erstelltes_spiel = Spiel(paar, team_1, team_2, runde,gespielt)
    return erstelltes_spiel

def turnier_setup():
    """
    erstellt die Objekte für jedes Team
    wenn es eine gruppen.csv gibt werden hieraus die Daten der Gruppen Erstellt
    """
    turniername = input("Turniername angeben: ")
    lokal_teams = []
    if os.path.isdir(f"turniere/{turniername}"):
        data_gruppen_csv = pandas.read_csv(f"turniere/{turniername}/gruppen.csv")
        print("turnier wurde gefunden")
        name_des_teamsn = data_gruppen_csv.teams.to_list()
        gruppe_des_teams = data_gruppen_csv.gruppe.to_list()
        for i in range(0,len(name_des_teamsn)):
            lokal_teams.append(neues_team(name_des_teamsn[i], gruppe_des_teams[i]))
        return data_gruppen_csv, turniername, lokal_teams
    else:
        print("kein turnier gefunden... ein neues turnier wird angelegt")
        os.mkdir(f"turniere/{turniername}")
        weitere_teams_anlegen = True
        while weitere_teams_anlegen:
            weitere_anlage = input("möchtest du ein neues Team Anlegen? (J/N): ")
            if  weitere_anlage == "N" or weitere_anlage == "n":
                weitere_teams_anlegen = False
            else:
                name_des_teams = input("Team Name angeben: ")
                gruppe_des_teams = input("in welcher Gruppe soll das Team Spielen?: ")
                if len(gruppe_des_teams) == 0:
                    gruppe_des_teams = 0
                lokal_teams.append(neues_team(name_des_teams, gruppe_des_teams))

        teams_dict = {
            "teams": [t.name for t in lokal_teams],
            "gruppe": [t.gruppe for t in lokal_teams]
        }
        data_gruppen_csv = pandas.DataFrame(teams_dict)
        data_gruppen_csv.to_csv(f"turniere/{turniername}/gruppen.csv", index = False)
        return data_gruppen_csv, turniername, lokal_teams

def runden_csv_erstellen(turniername, runden_lokal):
    """
    erstellung des runden.csv aus den Spielen aller Runden
    """
    runden_dict = {}
    for runden_jeder_gruppe in runden_lokal:
        for runde_der_gruppe in runden_jeder_gruppe:
            for spiele_der_runde in runde_der_gruppe.spiele:
                runden_dict[spiele_der_runde.paar] = spiele_der_runde.team_1.gruppe.name, spiele_der_runde.runde, spiele_der_runde.gespielt, spiele_der_runde.ergebnis

    data_runden_csv = pandas.DataFrame(runden_dict)
    data_runden_csv.to_csv(f"turniere/{turniername}/runden.csv", index = False)
    return data_runden_csv

def gruppen_anlage(data_gruppen_csv, turniername, teams_lokal):
    """
    erstellt die Objekte für jede Gruppe
    wenn die runden.csv die Runden aus und erstellt die Objekte für jede Runde und Spiele jeder Gruppe
    """
    gruppen_lokal = []
    gruppen_in_csv = data_gruppen_csv.gruppe.unique().tolist()
    print(f"gruppen die mitspielen: {gruppen_in_csv}")

    if os.path.isfile(f"turniere/{turniername}/runden.csv"):
        data_runden_csv = pandas.read_csv(f"turniere/{turniername}/runden.csv")
        print("es liegt ein Rundenplan vor")
        data_runden = data_runden_csv.to_dict()

        for gruppe_aus_gruppen in gruppen_in_csv:
            runden_werden_gespielt = 0
            for key, value in data_runden.items():
                paar_des_spieles   = key
                gruppe_des_spieles = value [0]
                runde              = value [1]
                gespielt           = value [2]
                ergebnis           = value [3]

                if int(runde) > runden_werden_gespielt and gruppe_des_spieles == gruppe_aus_gruppen:
                    runden_werden_gespielt = int(runde)

            teams_in_gruppe = []
            for teams_aus_csv in data_gruppen_csv[data_gruppen_csv.gruppe == gruppe_aus_gruppen].teams.tolist():
                for team_aus_teams in teams_lokal:
                    if teams_aus_csv == team_aus_teams.name:
                        teams_in_gruppe.append(team_aus_teams)
                        break
            gruppen_lokal.append(neue_gruppe(gruppe_aus_gruppen,int(runden_werden_gespielt),teams_in_gruppe))
        return gruppen_lokal

    else:
        for gruppe_aus_csv in gruppen_in_csv:
            anzahl_der_teams = len(data_gruppen_csv[data_gruppen_csv.gruppe == gruppe_aus_csv])

            runden_werden_gespielt = input("wie viele Runden werden gespielt? (n/e/d): ")
            if runden_werden_gespielt[0] == "e":
                runden_werden_gespielt = anzahl_der_teams/2*(anzahl_der_teams-1)
            else:
                if runden_werden_gespielt[0] == "d":
                    runden_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)
                elif runden_werden_gespielt > anzahl_der_teams*(anzahl_der_teams-1):
                    runden_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)

            print(f"es werden {int(runden_werden_gespielt)} runden in dieser Gruppe gespielt")

            teams_in_gruppe = []
            for teams_aus_csv in data_gruppen_csv[data_gruppen_csv.gruppe == gruppe_aus_csv].teams.tolist():
                for team_aus_teams in teams_lokal:
                    if teams_aus_csv == team_aus_teams.name:
                        teams_in_gruppe.append(team_aus_teams)
                        break

            gruppen_lokal.append(neue_gruppe(gruppe_aus_csv,int(runden_werden_gespielt),teams_in_gruppe))

    for team_aus_teams in teams_lokal:
        for gruppe_aus_gruppen in gruppen_lokal:
            if team_aus_teams.gruppe == gruppe_aus_gruppen.name:
                team_aus_teams.gruppe_aendern(gruppe_aus_gruppen)
    return gruppen_lokal

def spielplan_erstellen(turniername, teams_lokal, gruppen_lokal):
    """
    erstellt die Objekte für jede Runde und Spiele jeder Gruppe
    außerdem wird die erstmalige erstellung der runden.csv aufgerufen
    """
    runden_lokal = []
    for gruppe_aus_gruppen in gruppen_lokal:
        print(f"gruppe: {gruppe_aus_gruppen.name}")
        teams_in_gruppe = []
        for teams_aus_gruppe in gruppe_aus_gruppen.teams_in_gruppe:
            teams_in_gruppe.append(teams_aus_gruppe.name)

        if len(teams_in_gruppe) % 2 > 0:
            filler_team = "-"+str(gruppe_aus_gruppen.name)
            teams_in_gruppe.append(filler_team)
            teams_lokal.append(neues_team(filler_team, gruppe_aus_gruppen))
            gruppe_aus_gruppen.teams_aendern(team for team in teams_lokal if team.gruppe == gruppe_aus_gruppen.name)

        random.shuffle(teams_in_gruppe)

        paare_der_hinrunde = []
        paare_der_rueckrunde = []
        for i in range(len(teams_in_gruppe)):
            for j in range(i+1, len(teams_in_gruppe)):
                paare_der_hinrunde.append((teams_in_gruppe[i], teams_in_gruppe[j]))
                paare_der_rueckrunde.append((teams_in_gruppe[j], teams_in_gruppe[i]))
        alle_runden = paare_der_hinrunde + paare_der_rueckrunde

        runden_aufsetzen = {}
        runden_counter = 0
        runden_aktuelle_gruppe = []
        while runden_counter < gruppe_aus_gruppen.spieleanzahl:
            runden_counter += 1
            paare_der_runden = []
            teams_haben_gespielt = []
            for paar in alle_runden:
                team1, team2 = paar
                schon_gespielt = False
                for key, value in runden_aufsetzen.items():
                    if paar in value:
                        schon_gespielt = True

                if not schon_gespielt and team1 not in teams_haben_gespielt and team2 not in teams_haben_gespielt:
                    paare_der_runden.append(paar)
                    teams_haben_gespielt.append(team1)
                    teams_haben_gespielt.append(team2)

            runden_aufsetzen[runden_counter] = paare_der_runden

        runden_counter = 0
        for runde_aus_aufsetzen_dict in runden_aufsetzen:
            runden_counter += 1
            spiele_in_runde = []
            for paar in runden_aufsetzen[runde_aus_aufsetzen_dict]:
                team_1, team_2 = paar
                for team_aus_teams in teams_lokal:
                    if team_1 == team_aus_teams.name:
                        team_1 = team_aus_teams
                    if team_2 == team_aus_teams.name:
                        team_2 = team_aus_teams
                paar = f"{team_1.name}/{team_2.name}"
                spiele_in_runde.append(neues_spiel(paar,team_1,team_2,runden_counter, False))

            runden_aktuelle_gruppe.append(neue_runde(runde_aus_aufsetzen_dict,spiele_in_runde))

        runden_lokal.append(runden_aktuelle_gruppe)

        for runde_der_gruppe in runden_aktuelle_gruppe:
            print(f"Rundenr: {runde_der_gruppe.rundenzahl}")
            for spiele_der_runde in runde_der_gruppe.spiele:
                print(f"es spielen: {spiele_der_runde.paar}")
        print("-----")
        runden_csv_erstellen(turniername, runden_lokal)
    return runden_lokal

def runden_daten_aus_csv(turniername, gruppen_lokal):
    """
    liest aus der runden.csv die Runden aus und erstellt die Objekte für jede Runde und Spiele jeder Gruppe
    """
    schon_gespielt = False
    runden_lokal = []

    data_runden_csv = pandas.read_csv(f"turniere/{turniername}/runden.csv")
    data_runden = data_runden_csv.to_dict()

    for gruppe_aus_gruppen in gruppen_lokal:
        runden_aktuelle_gruppe = []
        spiele_in_runde = []
        aktuelle_runde = 1
        for key, value in data_runden.items():
            paar_des_spieles   = key
            gruppe_des_spieles = value [0]
            runde_aus_csv      = value [1]
            gespielt           = value [2]
            ergebnis_str       = value [3]

            paar_des_spieles_split = paar_des_spieles.split("/")
            runde_aus_csv = int(runde_aus_csv)
            ergebnis_str = ergebnis_str.replace("[","")
            ergebnis_str = ergebnis_str.replace("]","")
            ergebnis_str = ergebnis_str.replace(",","")
            ergebnis = [int(i) for i in ergebnis_str if i != " "]

            team_1 = ""
            team_2 = ""
            if gruppe_aus_gruppen.name == gruppe_des_spieles:
                for team_aus_gruppe in gruppe_aus_gruppen.teams_in_gruppe:
                    if team_aus_gruppe.name == paar_des_spieles_split[0]:
                        team_1 = team_aus_gruppe
                    elif team_aus_gruppe.name == paar_des_spieles_split[1]:
                        team_2 = team_aus_gruppe

                if runde_aus_csv == aktuelle_runde:
                    generiere_spiel = neues_spiel(paar_des_spieles,team_1,team_2,int(runde_aus_csv),gespielt)
                    spiele_in_runde.append(generiere_spiel)
                    if gespielt:
                        schon_gespielt = True
                        spiele_in_runde[-1] = spiele_in_runde[-1].ergebnis_aus_csv()
                else:
                    runden_aktuelle_gruppe.append(neue_runde(runde_aus_csv,spiele_in_runde))
                    aktuelle_runde = runde_aus_csv

        runden_lokal.append(runden_aktuelle_gruppe)

    if schon_gespielt:
        print("es wurden schon runden gespielt")
    return runden_lokal

def main():
    """
    main Funktion
    """
    teams = []
    gruppen = []
    runden = []

    welcome()
    data_gruppen_csv, turniername, teams = turnier_setup()
    gruppen = gruppen_anlage(data_gruppen_csv, turniername, teams)

    if not os.path.isfile(f"turniere/{turniername}/runden.csv"):
        runden = spielplan_erstellen(turniername, teams, gruppen)
    else:
        runden = runden_daten_aus_csv(turniername, gruppen)

if __name__ == "__main__":
    main()
