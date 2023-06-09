"""
Ablaufsteuerung des Turnierplans
"""
import os
import random
import pandas as pd

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


def turnier_setup():
    """erstellt die Objekte für jedes Team
    wenn es eine gruppen.json gibt werden hieraus die Daten der Gruppen Erstellt

    Returns:
        turniername str: turniername (Der name des Turnieres)
        teams_lokal list: Eine Liste aller Team Objekte
    """
    eingabe_erkannt = False
    while not eingabe_erkannt:
        turniername = input("Turniername angeben:\n")
        if turniername.isspace() or not turniername.isprintable():
            print("ungueltige eingabe")
        else:
            eingabe_erkannt = True

    teams_lokal = []
    if os.path.isfile(f"turniere/{turniername}/gruppen.json"):
        data_gruppen_json = pd.read_json(f"turniere/{turniername}/gruppen.json")
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
                teams_lokal.append(team)
        return turniername, teams_lokal
    else:
        print("kein turnier gefunden... ein neues turnier wird angelegt")
        if not os.path.isdir(f"turniere/{turniername}"):
            os.mkdir(f"turniere/{turniername}")
        weitere_teams_anlegen = True
        while weitere_teams_anlegen:
            weitere_anlage = input("möchtest du ein neues Team Anlegen? (J/N):\n").lower()
            if  weitere_anlage == "n":
                weitere_teams_anlegen = False
            else:
                check_eingabe = False
                while not check_eingabe:
                    eingabe_erkannt = False
                    while not eingabe_erkannt:
                        name_des_teams = input("Team Name angeben:\n")
                        if name_des_teams.isspace() or not name_des_teams.isprintable():
                            print("ungueltige eingabe")
                        else:
                            eingabe_erkannt = True
                    eingabe_erkannt = False
                    while not eingabe_erkannt:
                        gruppe_des_teams = input("in welcher Gruppe soll das Team Spielen?:\n")
                        if name_des_teams.isspace() or not name_des_teams.isprintable():
                            print("ungueltige eingabe")
                        else:
                            eingabe_erkannt = True
                    bestaetigung_eingabe = input(f"das team: {name_des_teams}\nspielt in: {gruppe_des_teams}\nist das korrekt? (J/N):\n").lower()
                    if bestaetigung_eingabe == "j" or bestaetigung_eingabe == "y"  or bestaetigung_eingabe == "y" :
                        check_eingabe = True

                if len(gruppe_des_teams) == 0:
                    gruppe_des_teams = 0
                neues_team = Team(name=name_des_teams, gruppe=gruppe_des_teams,punkte=0,treffer=0,gegentreffer=0)
                teams_lokal.append(neues_team)
        dataframe = pd.DataFrame(data=teams_lokal)
        dataframe.to_json(f"turniere/{turniername}/gruppen.json")
        return turniername, teams_lokal


def runden_json_erstellen(turniername, runden_lokal, teams_lokal):
    """erstellung des runden.json aus den Spielen aller Runden

    Args:
        turniername  str: Name des Turnieres
        runden_lokal list: Liste aller Runden Objekte
        teams_lokal  list: Liste aller Team Objekte
    """
    for runden_der_gruppen in runden_lokal:
        for runde_aus_runden in runden_der_gruppen:
            for spiel_aus_spielen in runde_aus_runden.spiele:
                spiel_aus_spielen.team_1 = spiel_aus_spielen.team_1.name
                spiel_aus_spielen.team_2 = spiel_aus_spielen.team_2.name

    dataframe = pd.DataFrame(data=runden_lokal)
    dataframe.to_json(f"turniere/{turniername}/runden.json")

    for runden_der_gruppen in runden_lokal:
        for runde_aus_runden in runden_der_gruppen:
            for spiel_aus_spielen in runde_aus_runden.spiele:
                for team_aus_teams in teams_lokal:
                    if spiel_aus_spielen.team_1 == team_aus_teams.name:
                        spiel_aus_spielen.team_1 = team_aus_teams
                    if spiel_aus_spielen.team_2 == team_aus_teams.name:
                        spiel_aus_spielen.team_2 = team_aus_teams


def gruppen_anlage(turniername, teams_lokal):
    """erstellt die Objekte für jede Gruppe

    Args:
        turniername  str: Name des Turnieres
        teams_lokal  list: Liste aller Team Objekte
    """
    gruppen_lokal = []
    gruppen_in_turnier = {}

    for team_aus_teams in teams_lokal:
        if team_aus_teams.gruppe not in gruppen_in_turnier.keys():
            gruppen_in_turnier[team_aus_teams.gruppe] = 1
        else:
            gruppen_in_turnier[team_aus_teams.gruppe] += 1

    for gruppe_aus_json,anzahl_der_teams in gruppen_in_turnier.items():
        if anzahl_der_teams % 2 > 0:
            filler_team = "-"+gruppe_aus_json
            teams_lokal.append(Team(name=filler_team, gruppe=gruppe_aus_json,punkte=0,treffer=0,gegentreffer=0))
            gruppen_in_turnier[gruppe_aus_json] += 1

        spiele_werden_gespielt = 0

        if not os.path.isfile(f"turniere/{turniername}/runden.json"):
            eingabe_erkannt = False
            while not eingabe_erkannt:
                runden_anfrage_modus = input('''[h] = Hinrunde\n[r] = Hin- und Rueckrunde\n[0-9] = Nummerische Eingabe
(wenn Num Eingabe > Hin- und Rueckrunde dann wird [r] verwendet)
wie viele Runden werden gespielt?: ''')

                if runden_anfrage_modus.isdigit():
                    spiele_werden_gespielt = int(runden_anfrage_modus)
                    if spiele_werden_gespielt > anzahl_der_teams*(anzahl_der_teams-1):
                        spiele_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)
                    eingabe_erkannt = True
                elif runden_anfrage_modus[0].lower() == "r":
                    spiele_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)
                    eingabe_erkannt = True
                elif runden_anfrage_modus[0].lower() == "h":
                    spiele_werden_gespielt = anzahl_der_teams/2*(anzahl_der_teams-1)
                    eingabe_erkannt = True
                else:
                    print("eingabe nicht erkannt")

            print(f"es werden {spiele_werden_gespielt} spiele in dieser Gruppe gespielt")

        teams_in_gruppe = []
        for team_aus_teams in teams_lokal:
            if gruppe_aus_json == team_aus_teams.gruppe:
                teams_in_gruppe.append(team_aus_teams)

        gruppen_lokal.append(Gruppe(gruppe_aus_json,spiele_werden_gespielt,teams_in_gruppe))

    for team_aus_teams in teams_lokal:
        for gruppe_aus_gruppen in gruppen_lokal:
            if team_aus_teams.gruppe == gruppe_aus_gruppen.name:
                team_aus_teams.gruppe_aendern(gruppe_aus_gruppen)
    return gruppen_lokal, teams_lokal


def spielplan_erstellen(turniername,teams_lokal, gruppen_lokal):
    """erstellt die Objekte für jede Runde und Spiele jeder Gruppe
    außerdem wird die erstmalige erstellung der runden.json aufgerufen

    Args:
        turniername   str: Name des Turnieres
        teams_lokal   list: Liste aller Team Objekte
        gruppen_lokal list: Liste aller Gruppen Objekte

    Returns:
        runden_lokal            list: Liste aller Team Objekte
        runden_sind_eingetragen dic: Der aktuelle Status der Spieleeintragung
    """
    runden_lokal = []
    runden_sind_eingetragen = {}

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
        spiele_counter = 0
        runden_aktuelle_gruppe = []
        while spiele_counter != gruppe_aus_gruppen.spieleanzahl:
            runden_counter += 1
            paare_der_runden = []
            teams_haben_gespielt = []
            for paar in alle_runden:
                team_1, team_2 = paar
                schon_gespielt = False
                for _, value in runden_aufsetzen.items():
                    if paar in value:
                        schon_gespielt = True

                if not schon_gespielt and team_1 not in teams_haben_gespielt and team_2 not in teams_haben_gespielt:
                    paare_der_runden.append(paar)
                    teams_haben_gespielt.append(team_1)
                    teams_haben_gespielt.append(team_2)
                    spiele_counter += 1

            runden_aufsetzen[runden_counter] = paare_der_runden

        runden_counter = 0
        for runde_des_aufsetzen, spiele_der_runde in runden_aufsetzen.items():
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
                spiele_lokal.append(Spiel(paar,team_1,team_2,runden_counter, False, [0,0]))

            runden_aktuelle_gruppe.append(Runde(runde_des_aufsetzen,spiele_lokal, False, gruppe_aus_gruppen.name))

        for runde_der_gruppe in runden_aktuelle_gruppe:
            print(f"Rundenr: {runde_der_gruppe.rundenzahl}")
            for spiele_der_runde in runde_der_gruppe.spiele:
                print(f"es spielen: {spiele_der_runde.paar}")
        print("-----")

        runden_lokal.append(runden_aktuelle_gruppe)

        #um zu tracken in welcher runde der Eintragung wir sind
        runden_sind_eingetragen[gruppe_aus_gruppen.name] = {"runde_eintragen":0,
                                                            "max_runden": runden_counter}

    runden_json_erstellen(turniername, runden_lokal, teams_lokal)
    return runden_lokal, runden_sind_eingetragen


def runden_daten_aus_json(turniername, teams_lokal, gruppen_lokal):
    """liest aus der runden.json die Runden und Gruppen aus und
    erstellt die Objekte für jede Runde und Spiel

    Args:
        turniername   str: Name des Turnieres
        teams_lokal   list: Liste aller Team Objekte
        gruppen_lokal list: Liste aller Gruppen Objekte

    Returns:
        runden_lokal            list: Liste aller Team Objekte
        runden_sind_eingetragen dic: Der aktuelle Status der Spieleeintragung
    """
    print("es liegt ein Rundenplan vor")
    runden_lokal = []

    data_runden_json = pd.read_json(f"turniere/{turniername}/runden.json")

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

    for runden_der_gruppe in runden_lokal:
        runden_counter = 0
        for runde_aus_runden in runden_der_gruppe:
            runden_counter += 1
            for spiel_aus_spielen in runde_aus_runden.spiele:
            #Zuordnung der Teamobjekte zu den jeweiligen Spielen
                for team_aus_teams in teams_lokal:
                    if spiel_aus_spielen.team_1 == team_aus_teams.name:
                        spiel_aus_spielen.team_1 = team_aus_teams
                    if spiel_aus_spielen.team_2 == team_aus_teams.name:
                        spiel_aus_spielen.team_2 = team_aus_teams
        runde_aus_runden.spiele[0].team_1.gruppe.spieleanzahl = runden_counter

    runden_sind_eingetragen = {}

    for runden_der_gruppe in runden_lokal:
        for runde_aus_runden in runden_der_gruppe:
            runden_sind_eingetragen[runde_aus_runden.gruppe_der_runde] = {"runde_eintragen":runde_aus_runden.rundenzahl - 1,
                                                                          "max_runden": runde_aus_runden.spiele[0].team_1.gruppe.spieleanzahl}
            if not runde_aus_runden.runde_gespielt:
                break


            for spiel_aus_spielen in runde_aus_runden.spiele:
                if spiel_aus_spielen.gespielt:
                    spiel_aus_spielen.ergebnis_eintragen(spiel_aus_spielen.ergebnis[0], spiel_aus_spielen.ergebnis[1])

    return runden_lokal, runden_sind_eingetragen


def spiel_eintragen(runden_sind_eingetragen, runden_lokal):
    """ eintragen der Ergebnise in die Spiele, sowie Anpassung der Punkte der Teams
    anfrage, fuer welche Gruppe und welches Spiel der Runde eine Eintragung stattfinden soll
    eintragung der Ergebnise und vermerkung dieser in den Teams

    Args:
        runden_sind_eingetragen dic: Der aktuelle Status der Spieleeintragung
        runden_lokal            list: Liste aller Team Objekte

    Returns:
        runden_sind_eingetragen dic: Der aktuelle Status der Spieleeintragung
        runden_lokal            list: Liste aller Team Objekte
    """
    for index_gruppe, (name_der_gruppe, aktuelle_runde) in enumerate(runden_sind_eingetragen.items()):
        print(f"[{index_gruppe}]: gruppe {name_der_gruppe}")

    eingabe_erkannt = False
    while not eingabe_erkannt:
        eingabe_gruppe = input("bei welcher Gruppe?: ")
        if eingabe_gruppe.isdigit():
            eingabe_gruppe = int(eingabe_gruppe)
            if eingabe_gruppe > len(runden_lokal):
                print("Gruppe nicht gefunden")
            else:
                eingabe_erkannt = True

    runde_aktuell_und_max = {}
    for index_gruppe, (name_der_gruppe, runde_aktuell_und_max) in enumerate(runden_sind_eingetragen.items()):
        if index_gruppe == eingabe_gruppe:
            break

    runde_eintragen = runde_aktuell_und_max["runde_eintragen"]

    if runde_eintragen == runde_aktuell_und_max["max_runden"]:
        print("es gibt bei dieser Gruppe keine Spiele mehr")
        return runden_sind_eingetragen, runden_lokal
    else:
        print(f"wir befinden uns in runde {runde_eintragen}")

    for index, spiel_aus_spielen in enumerate(runden_lokal[eingabe_gruppe][runde_eintragen].spiele):
        if (spiel_aus_spielen.team_1.name[0] == "-" or spiel_aus_spielen.team_2.name[0] == "-"
        and not spiel_aus_spielen.gespielt):
            spiel_aus_spielen.gespielt = True

        if spiel_aus_spielen.gespielt:
            print(f"[{index}]: {spiel_aus_spielen.paar} ergebnis: {spiel_aus_spielen.ergebnis}")
        else:
            print(f"[{index}]: {spiel_aus_spielen.paar}")

    eingabe_erkannt = False
    while not eingabe_erkannt:
        eingabe_spiel = input("bei welchem Spiel?: ")
        if eingabe_spiel.isdigit():
            eingabe_spiel = int(eingabe_spiel)
            if eingabe_spiel > len(runden_lokal[eingabe_gruppe][runde_eintragen].spiele):
                print("Spiel nicht gefunden")
            else:
                eingabe_erkannt = True

    runden_lokal[eingabe_gruppe][runde_eintragen].runde_gespielt = True

    spiel_der_eingabe = runden_lokal[eingabe_gruppe][runde_eintragen].spiele[eingabe_spiel]

    ergebnis_des_spieles = []
    eingabe_erkannt = False
    while not eingabe_erkannt:
        eingabe_punkte = input(f"wie viele treffer hat {spiel_der_eingabe.team_1.name} gemacht?: ")
        if eingabe_punkte.isdigit():
            ergebnis_des_spieles.append(int(eingabe_punkte))
        else:
            ergebnis_des_spieles.append(0)
        eingabe_punkte = input(f"wie viele treffer hat {spiel_der_eingabe.team_2.name} gemacht?: ")
        if eingabe_punkte.isdigit():
            ergebnis_des_spieles.append(int(eingabe_punkte))
        else:
            ergebnis_des_spieles.append(0)
        bestaetigung_eingabe = input(f"das ergebnis ist also: {ergebnis_des_spieles}\nist das korrekt? (J/N):\n").lower()
        if bestaetigung_eingabe == "j" or bestaetigung_eingabe == "y" :
            eingabe_erkannt = True

    if not (spiel_der_eingabe.team_1.name.startswith("-") or spiel_der_eingabe.team_2.name.startswith("-")):
        spiel_der_eingabe.ergebnis_eintragen(ergebnis_des_spieles[0], ergebnis_des_spieles[1])

    rundenzahl_erhoehen = True
    for spiel_aus_spielen in runden_lokal[eingabe_gruppe][runde_eintragen].spiele:
        if not spiel_aus_spielen.gespielt:
            rundenzahl_erhoehen = False

    if rundenzahl_erhoehen:
        print("alle spiele dieser Runde sind eingetragen")
        eingabe_erkannt = False
        while not eingabe_erkannt:
            eingabe_runden_erhoehen = input("soll die runde abgeschlossen werden? (J/N):\n").lower()
            if eingabe_runden_erhoehen == "j" or eingabe_runden_erhoehen == "y":
                runden_sind_eingetragen[name_der_gruppe]["runde_eintragen"] = runde_eintragen + 1
                eingabe_erkannt = True
            elif eingabe_runden_erhoehen == "n":
                eingabe_erkannt = True
            else:
                print("ungueltige eingabe")


def tabelle_erstellen(gruppen_lokal):
    """zusammenstellung der aktuellen tabelle

    Args:
        gruppen_lokal list: Liste aller Gruppen Objekte

    Returns:
        tabelle_lokal dic: Sortiertes Dictonary des aktuellen Tabellenstandes je Gruppe
    """
    #je gruppe team: name punktzahl und tordifferenz
    tabelle_lokal = {}
    for gruppe_aus_gruppen in gruppen_lokal:
        aktuelle_gruppe = {}
        for team_aus_teams in gruppe_aus_gruppen.teams_in_gruppe:
            aktuelle_gruppe[team_aus_teams.name] = {"punkte":team_aus_teams.punkte,
                                                    "treffer_diff": team_aus_teams.treffer - team_aus_teams.gegentreffer}
        tabelle_lokal[gruppe_aus_gruppen.name] = aktuelle_gruppe

    for gruppe_der_tabelle in tabelle_lokal:
        tabelle_lokal[gruppe_der_tabelle] = sorted(tabelle_lokal[gruppe_der_tabelle].items(), key=lambda x: (x[1]['punkte'], x[1]['treffer_diff']), reverse=True)
        tabelle_lokal[gruppe_der_tabelle] = dict(tabelle_lokal[gruppe_der_tabelle])

    return tabelle_lokal


def tabelle_darstellen(tabelle_lokal):
    """
    darstellung einer Tabelle
    """
    for gruppe_der_tabelle, teams_der_tabelle in tabelle_lokal.items():
        print("-------------------------------------------------------")
        print("| Position | Team              | Punkte | Trefferdiff |")
        print("|----------|-------------------|--------|-------------|")
        print(f"| {'gruppe ' + gruppe_der_tabelle:^42}          |")
        print("|----------|-------------------|--------|-------------|")
        index_position = 0
        for team_in_gruppe, stats_des_teams in teams_der_tabelle.items():
            index_position += 1
            print(f"|    {index_position:2}    | {team_in_gruppe:<16}  |   {stats_des_teams['punkte']:2}   |     {stats_des_teams['treffer_diff']:3}     |")
            #right-aligned in field with    left-aligned

        print("-------------------------------------------------------\n")


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
        runden, runden_sind_eingetragen = runden_daten_aus_json(turniername, teams, gruppen)
    else:
        runden, runden_sind_eingetragen = spielplan_erstellen(turniername, teams, gruppen)

    running = True
    while running:
        next_action = input("""aktionen:
[0]: Spiel eintragen\n[1]: Tabelle generieren\n[2]: Speichern des Turnieres\n[3]: Stop das Programm
""")
        if next_action == "0":
            print("es werden spiele eingetragen")
            spiel_eintragen(runden_sind_eingetragen, runden)
        elif next_action == "1":
            print("die tabelle wird generiert...\n")
            tabelle = tabelle_erstellen(gruppen)
            tabelle_darstellen(tabelle)
        elif next_action == "2":
            print("der aktuelle Stand wird gespeichert")
            runden_json_erstellen(turniername, runden, teams)
        elif next_action == "3":
            running = False
        else:
            print("eingabe nicht erkannt")

if __name__ == "__main__":
    main()
