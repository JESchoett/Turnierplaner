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

def neue_runde(rundenzahl, spiele, runde_gespielt, gruppe_der_runde):
    """
    anlage eines Runde Objektes
    """
    erstellte_runde = Runde(rundenzahl, spiele, runde_gespielt, gruppe_der_runde)
    return erstellte_runde

def neues_spiel(paar, team_1, team_2, runde, gespielt, ergebnis):
    """
    anlage eines Spiel Objektes
    """
    erstelltes_spiel = Spiel(paar, team_1, team_2, runde,gespielt, ergebnis)
    return erstelltes_spiel

def turnier_setup():
    """
    erstellt die Objekte für jedes Team
    wenn es eine gruppen.json gibt werden hieraus die Daten der Gruppen Erstellt
    """
    turniername = input("Turniername angeben: ")
    lokal_teams = []
    if os.path.isfile(f"turniere/{turniername}/gruppen.json"):
        data_gruppen_json = pandas.read_json(f"turniere/{turniername}/gruppen.json")
        print("turnier wurde gefunden")
        for column in data_gruppen_json:
            for _, team_data in data_gruppen_json[column].items():
                team = Team(
                    name         = team_data["name"],
                    gruppe       = team_data["gruppe"],
                    punkte       = team_data.get("punkte", 0),
                    treffer      = team_data.get("treffer", 0),
                    gegentreffer = team_data.get("gegentreffer", 0)
                )
                lokal_teams.append(team)
        return turniername, lokal_teams
    else:
        print("kein turnier gefunden... ein neues turnier wird angelegt")
        os.mkdir(f"turniere/{turniername}")
        weitere_teams_anlegen = True
        while weitere_teams_anlegen:
            weitere_anlage = input("möchtest du ein neues Team Anlegen? (J/N): ").lower()
            if  weitere_anlage == "n":
                weitere_teams_anlegen = False
            else:
                name_des_teams = input("Team Name angeben: ")
                gruppe_des_teams = input("in welcher Gruppe soll das Team Spielen?: ")
                if len(gruppe_des_teams) == 0:
                    gruppe_des_teams = 0
                lokal_teams.append(neues_team(name_des_teams, gruppe_des_teams))
        dataframe = pandas.DataFrame(data=lokal_teams)
        dataframe.to_json(f"turniere/{turniername}/gruppen.json")
        return turniername, lokal_teams

def runden_json_erstellen(turniername, runden_lokal):
    """
    erstellung des runden.json aus den Spielen aller Runden
    """
    for runden_der_gruppen in runden_lokal:
        for runden_aus_runden in runden_der_gruppen:
            for spiel_aus_spielen in runden_aus_runden.spiele:
                spiel_aus_spielen.team_1 = spiel_aus_spielen.team_1.name
                spiel_aus_spielen.team_2 = spiel_aus_spielen.team_2.name

    dataframe = pandas.DataFrame(data=runden_lokal)
    dataframe.to_json(f"turniere/{turniername}/runden.json")

def gruppen_anlage(turniername, teams_lokal):
    """
    erstellt die Objekte für jede Gruppe
    """
    gruppen_lokal = []
    gruppen_in_turnier = {}

    for team_aus_teams in teams_lokal:
        if team_aus_teams.gruppe not in gruppen_in_turnier.keys():
            gruppen_in_turnier[team_aus_teams.gruppe] = 1
        else:
            gruppen_in_turnier[team_aus_teams.gruppe] += 1

    print(f"gruppen die mitspielen: {gruppen_in_turnier}")

    for gruppe_aus_json,anzahl_der_teams in gruppen_in_turnier.items():
        if anzahl_der_teams % 2 > 0:
            filler_team = "-"+gruppe_aus_json
            teams_lokal.append(neues_team(filler_team, gruppe_aus_json))
            gruppen_in_turnier[gruppe_aus_json] += 1

        runden_werden_gespielt = 0

        if not os.path.isfile(f"turniere/{turniername}/runden.json"):
            runden_anfrage_modus = input("wie viele Runden werden gespielt? (h = Hinrunde/r = Rückrunde): ").lower()
            if runden_anfrage_modus[0] == "r":
                runden_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)
            else:
                runden_werden_gespielt = anzahl_der_teams/2*(anzahl_der_teams-1)

            print(f"es werden {runden_werden_gespielt} runden in dieser Gruppe gespielt")

        teams_in_gruppe = []
        for team_aus_teams in teams_lokal:
            if gruppe_aus_json == team_aus_teams.gruppe:
                teams_in_gruppe.append(team_aus_teams)

        gruppen_lokal.append(neue_gruppe(gruppe_aus_json,runden_werden_gespielt,teams_in_gruppe))

    for team_aus_teams in teams_lokal:
        for gruppe_aus_gruppen in gruppen_lokal:
            if team_aus_teams.gruppe == gruppe_aus_gruppen.name:
                team_aus_teams.gruppe_aendern(gruppe_aus_gruppen)
    return gruppen_lokal, teams_lokal

def spielplan_erstellen(turniername,teams_lokal, gruppen_lokal):
    """
    erstellt die Objekte für jede Runde und Spiele jeder Gruppe
    außerdem wird die erstmalige erstellung der runden.json aufgerufen
    """
    runden_lokal = []
    for gruppe_aus_gruppen in gruppen_lokal:
        print(f"gruppe: {gruppe_aus_gruppen.name}")
        teams_in_gruppe = []
        for teams_aus_gruppe in gruppe_aus_gruppen.teams_in_gruppe:
            teams_in_gruppe.append(teams_aus_gruppe.name)

        random.shuffle(teams_in_gruppe)

        paare_der_hinrunde = []
        paare_der_rueckrunde = []
        for index_i,team_i in enumerate(teams_in_gruppe):
            for index_j,team_j in enumerate(teams_in_gruppe[index_i+1:], start=index_i+1):
                paare_der_hinrunde.append((team_i, team_j))
                paare_der_rueckrunde.append((team_j, team_i))
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
                for _, value in runden_aufsetzen.items():
                    if paar in value:
                        schon_gespielt = True

                if not schon_gespielt and team1 not in teams_haben_gespielt and team2 not in teams_haben_gespielt:
                    paare_der_runden.append(paar)
                    teams_haben_gespielt.append(team1)
                    teams_haben_gespielt.append(team2)

            runden_aufsetzen[runden_counter] = paare_der_runden

        runden_counter = 0
        for runde_aus_aufsetzen, spiele_der_runde in runden_aufsetzen.items():
            runden_counter += 1
            spiele_lokal = []
            for paar in spiele_der_runde:
                team_1, team_2 = paar
                for team_aus_teams in teams_lokal:
                    if team_1 == team_aus_teams.name:
                        team_1 = team_aus_teams
                    if team_2 == team_aus_teams.name:
                        team_2 = team_aus_teams
                paar = f"{team_1.name}/{team_2.name}"
                spiele_lokal.append(neues_spiel(paar,team_1,team_2,runden_counter, False, [0,0]))

            runden_aktuelle_gruppe.append(neue_runde(runde_aus_aufsetzen,spiele_lokal, False, gruppe_aus_gruppen.name))

        runden_lokal.append(runden_aktuelle_gruppe)

        for runde_der_gruppe in runden_aktuelle_gruppe:
            print(f"Rundenr: {runde_der_gruppe.rundenzahl}")
            for spiele_der_runde in runde_der_gruppe.spiele:
                print(f"es spielen: {spiele_der_runde.paar}")
        print("-----")
    runden_json_erstellen(turniername, runden_lokal)
    return runden_lokal

def runden_daten_aus_json(turniername, teams_lokal, gruppen_lokal):
    """
    liest aus der runden.json die Runden und Gruppen aus und erstellt die Objekte für jede Runde und Spiel
    """
    print("es liegt ein Rundenplan vor")
    runden_lokal = []

    data_runden_json = pandas.read_json(f"turniere/{turniername}/runden.json")

    #jede Gruppe hat in der runden liste eine liste mit den runden objekte der Gruppe
    for gruppe_aus_gruppen in gruppen_lokal:
        runden_der_gruppe = []
        for column in data_runden_json:
            for _, runden_daten in data_runden_json[column].items():
                if runden_daten is not None:
                    if gruppe_aus_gruppen.name == runden_daten["gruppe_der_runde"]:
                        runde = Runde(
                            rundenzahl       = runden_daten["rundenzahl"],
                            spiele           = runden_daten["spiele"],
                            runde_gespielt   = runden_daten["runde_gespielt"],
                            gruppe_der_runde = runden_daten["gruppe_der_runde"]
                        )
                        runden_der_gruppe.append(runde)
        runden_lokal.append(runden_der_gruppe)

    for runden_der_gruppe in runden_lokal:
        for runde_aus_runden in runden_der_gruppe:
            spiele_der_runde = []
            for spiel_daten in runde_aus_runden.spiele:
                spiel = Spiel(
                    paar     = spiel_daten["paar"],
                    team_1   = spiel_daten["team_1"],
                    team_2   = spiel_daten["team_2"],
                    runde    = spiel_daten["runde"],
                    gespielt = spiel_daten["gespielt"],
                    ergebnis = spiel_daten["ergebnis"]
                )
                spiele_der_runde.append(spiel)
            runde_aus_runden.spiele = spiele_der_runde

    teams_angepasst = []
    for runden_der_gruppe in runden_lokal:
        for runde_aus_runden in runden_der_gruppe:
            for spiel_aus_spielen in runde_aus_runden.spiele:
            #Zuordnung der Teamobjekte zu den jeweiligen Spielen
                for team_aus_teams in teams_lokal:
                    if team_aus_teams.name not in teams_angepasst:
                        if spiel_aus_spielen.team_1 == team_aus_teams.name:
                            spiel_aus_spielen.team_1 = team_aus_teams
                            teams_angepasst.append(team_aus_teams.name)
                        if spiel_aus_spielen.team_2 == team_aus_teams.name:
                            spiel_aus_spielen.team_2 = team_aus_teams
                            teams_angepasst.append(team_aus_teams.name)

            #punkte müssen vergeben werden
    for runden_der_gruppe in runden_lokal:
        for runde_aus_runden in runden_der_gruppe:
            if not runde_aus_runden.runde_gespielt:
                break
            for spiel_aus_spielen in runde_aus_runden.spiele:
                if spiel_aus_spielen.gespielt:
                    spiel_aus_spielen.ergebnis_eintragen(spiel_aus_spielen.ergebnis[0], spiel_aus_spielen.ergebnis[1])

    return runden_lokal

def main():
    """
    main Funktion
    """
    teams = []
    gruppen = []
    runden = []

    welcome()
    turniername, teams = turnier_setup()
    gruppen, teams = gruppen_anlage(turniername, teams)

    if os.path.isfile(f"turniere/{turniername}/runden.json"):
        runden = runden_daten_aus_json(turniername, teams, gruppen)
    else:
        runden = spielplan_erstellen(turniername, teams, gruppen)

    #test, der aufgebauten Daten
    for runden_der_gruppen in runden:
        for runden_aus_runden in runden_der_gruppen:
            print(runden_aus_runden.rundenzahl)
            for spiel_aus_spielen in runden_aus_runden.spiele:
                print(spiel_aus_spielen.paar)

    for gruppe_aus_gruppen in gruppen:
        print(gruppe_aus_gruppen.name)
        for team_aus_teams in gruppe_aus_gruppen.teams_in_gruppe:
            print(f"{team_aus_teams.name} hat {team_aus_teams.punkte} punkte")

if __name__ == "__main__":
    main()