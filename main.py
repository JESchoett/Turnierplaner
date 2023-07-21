"""
Aktuell store ich hier die Design Idee, bevor ich in main.py
das Design mit den Funktionalitäten des Skriptes zusammenbringe
"""
import os
import random
import pandas as pd
import customtkinter as ctk

#import der Klassen und Funktionen
from team import Team
from gruppe import Gruppe
from spiele import Spiel
from runde import Runde

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

#----- Definitionen der Funktionen für den Ablauf-----#

def turnier_setup(turniername, status_anlage, live_frame):
    """erstellt die Objekte für jedes Team
    wenn es eine gruppen.json gibt werden hieraus die Daten der Gruppen Erstellt

    Returns:
        teams_lokal   list: Eine Liste aller Team Objekte
        gruppen_lokal list: Eine Liste aller Gruppen Objekte
    """
    #Erstellung der Objekte für die Teams
    teams_lokal = []
    gruppen_lokal = []
    gruppen_in_turnier = {}

    def gruppen_anlage(teams_lokal, gruppen_lokal, gruppen_in_turnier):
        #erstellen des eines Zählers der Teams je Gruppe, ob ein Filler Team angelegt werden muss
        for team_aus_teams in teams_lokal:
            if team_aus_teams.gruppe not in gruppen_in_turnier:
                gruppen_in_turnier[team_aus_teams.gruppe] = 1
            else:
                gruppen_in_turnier[team_aus_teams.gruppe] += 1

        for gruppe_aus_dictonary, anzahl_der_teams in gruppen_in_turnier.items():
            #anlage eines Filler Teams, wenn nötig
            if anzahl_der_teams % 2 > 0:
                filler_team = "-"+gruppe_aus_dictonary
                teams_lokal.append(Team(name=filler_team, gruppe=gruppe_aus_dictonary,punkte=0,treffer=0,gegentreffer=0))
                gruppen_in_turnier[gruppe_aus_dictonary] += 1
                anzahl_der_teams += 1

            #analyse, welche Teams in einer Gruppe sind
            teams_in_gruppe = []
            for team_aus_teams in teams_lokal:
                if gruppe_aus_dictonary == team_aus_teams.gruppe:
                    teams_in_gruppe.append(team_aus_teams)

            spiele_werden_gespielt = 0
            if not os.path.isfile(f"turniere/{turniername}/runden.json"):
                eingabe_erkannt = False
                text_dialog = f"""Wie viele Runden sollen in Gruppe {gruppe_aus_dictonary} gespielt werden?:
[h]   = Hinrunde
[r]   = Hin- und Rueckrunde
[0-9] = Nummerische Eingabe
(wenn Eingabe > Hin- und Rueckrunde dann wird [r] verwendet)"""

                while not eingabe_erkannt:
                    dialog = ctk.CTkInputDialog(text=text_dialog, title="Test")
                    engabe_dialog = dialog.get_input()
                    if engabe_dialog.isdigit():
                        spiele_werden_gespielt = int(engabe_dialog)
                        #wenn die nummerische eingabe grüßer als "r" wird r genommen
                        if spiele_werden_gespielt > anzahl_der_teams*(anzahl_der_teams-1):
                            spiele_werden_gespielt = int(anzahl_der_teams*(anzahl_der_teams-1))
                        eingabe_erkannt = True
                    elif engabe_dialog.lower().startswith("h"):
                        spiele_werden_gespielt = int(anzahl_der_teams/2*(anzahl_der_teams-1))
                        eingabe_erkannt = True
                    elif engabe_dialog.lower().startswith("r"):
                        spiele_werden_gespielt = int(anzahl_der_teams*(anzahl_der_teams-1))
                        eingabe_erkannt = True

            #anlage des Gruppen Objektes
            gruppen_lokal.append(Gruppe(gruppe_aus_dictonary,spiele_werden_gespielt,teams_in_gruppe))

        #zuordnung der Team Objekte zu den Gruppen Objekten
        for team_aus_teams in teams_lokal:
            for gruppe_aus_gruppen in gruppen_lokal:
                if team_aus_teams.gruppe == gruppe_aus_gruppen.name:
                    team_aus_teams.gruppe_aendern(gruppe_aus_gruppen)
        return teams_lokal, gruppen_lokal

    if os.path.isfile(f"turniere/{turniername}/gruppen.json"):
        data_gruppen_json = pd.read_json(f"turniere/{turniername}/gruppen.json")
        print("turnier wurde gefunden")
        #anlage der Teams
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
        teams_lokal, gruppen_lokal = gruppen_anlage(teams_lokal, gruppen_lokal, gruppen_in_turnier)
    else:
        if status_anlage == "Turnier_Setup_neuanlage":
            for team_name, team_gruppe, ent_button in live_frame.entrys:
                teams_lokal.append(Team(name=team_name.get(), gruppe=team_gruppe.get(),punkte=0,treffer=0,gegentreffer=0))

            #anlage der Grupen.json
            dataframe = pd.DataFrame(data=teams_lokal)
            dataframe.to_json(f"turniere/{turniername}/gruppen.json")

            teams_lokal, gruppen_lokal = gruppen_anlage(teams_lokal, gruppen_lokal, gruppen_in_turnier)

    return teams_lokal, gruppen_lokal


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

        anzahl_teams = len(gruppe_aus_gruppen.teams_in_gruppe)

        if gruppe_aus_gruppen.spieleanzahl > int(anzahl_teams/2*(anzahl_teams-1)):
            alle_runden = paare_der_hinrunde + paare_der_rueckrunde
        else:
            alle_runden = paare_der_hinrunde

        runden_aufsetzen = {}
        runden_counter = 0
        spiele_counter = 0
        runden_aktuelle_gruppe = []
        while spiele_counter != gruppe_aus_gruppen.spieleanzahl:
            random.shuffle(alle_runden)
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


#----- Erstellung der Frames für das GUI -----#
class WillkommenFrame(ctk.CTkFrame):
    """Erstellen eines Frames zum Laden des Turnieres"""
    def __init__(self, master):
        super().__init__(master)

        self.listiner = 0
        self.label_welc = ctk.CTkLabel(self, text="Willkommen beim Turnierplaner", font=("Arial",30))
        self.label_welc.grid(row=0, column=0, padx=30, pady=(30,10), sticky="e", columnspan=4)

        self.label_2 = ctk.CTkLabel(self, text="Bitte Turniernamen eingeben: ", font=("Arial",15))
        self.label_2.grid(row=1, column=0, padx=10, pady=0, sticky="e")

        self.entry_turnier = ctk.CTkEntry(self, width=250)
        self.entry_turnier.grid(row=1, column=1, padx=10, pady=(20,30), sticky="w", columnspan=4)

        self.label_2 = ctk.CTkLabel(self, text="Gefundene Turniere: ", font=("Arial",15))
        self.label_2.grid(row=2, column=0, padx=10, pady=(0, 30), sticky="e")

        self.col_in_row = 0
        self.row_der_turniere = 2
        self.turniere = []


        #Für jeden gefunden Turnier Ordner wird ein Button generiert
        for turnier_dir in os.listdir("turniere"):
            if turnier_dir != "Test-Turnier":
                self.col_in_row += 1
                self.turniere.append(turnier_dir)
                command_func = lambda text=turnier_dir: self.turnier_name(text)
                #die Lamdafunktion ist hier und nicht im Button selber um für jedes Turnier eine eigene zu erstellen

                self.turnier_dir_btn = ctk.CTkButton(self, text=turnier_dir, command= command_func)
                self.turnier_dir_btn.grid(row=self.row_der_turniere, column=self.col_in_row, padx=10, pady=(0, 30), sticky="w")
                if self.col_in_row == 4:
                    self.col_in_row = 0
                    self.row_der_turniere += 1

    def turnier_name(self, text):
        """einfügen des Turniernamens in die Entry"""
        self.entry_turnier.delete(0, 250)
        self.entry_turnier.insert(0,text)


class TeamErstellenFrame(ctk.CTkFrame):
    """
    Erstellen eines Frames in dem Teams und Gruppen angelegt werden
    Außerdem wird die gruppen.json hier angelegt
    """
    def __init__(self, master):
        super().__init__(master)

        self.label_welc = ctk.CTkLabel(self, text="Anlage von Teams und Gruppen", font=("Arial",30))
        self.label_welc.grid(row=0, column=0, padx=(30,10), pady=(30,10), sticky="ew", columnspan=4)

        self.button_t = ctk.CTkButton(self, text="Team")
        self.button_t.grid(row=1, column=1, padx=(30,0), pady=(10, 0), sticky="ew")

        self.button_g = ctk.CTkButton(self, text="Gruppe")
        self.button_g.grid(row=1, column=2, padx=(0,30), pady=(10, 0), sticky="ew")

        self.weiteres_team_btn = ctk.CTkButton(master=self, text="Weiteres Team", command=self.weiteres_team)

        self.team_row = 1
        self.entrys = []
        self.weiteres_team()

    def weiteres_team(self):
        """Erstellung weiterer Entrys für die Eingabe eines neuen Teams
        """
        if len(self.entrys) > 0:
            self.entrys[-1][2].configure(state="disabled")

        self.label_team = ctk.CTkLabel(self, text=f"Team Nr. {self.team_row}")

        self.team_row += 1

        self.label_team.grid(row=self.team_row, column=0, padx=30, pady=0, sticky="e")

        self.entry_name_t = ctk.CTkEntry(self, width=10)
        self.entry_name_t.grid(row=self.team_row, column=1, padx=(30,0), pady=0, sticky="ew")

        self.entry_name_g = ctk.CTkEntry(self, width=30)
        self.entry_name_g.grid(row=self.team_row, column=2, padx=(0,30), pady=0, sticky="ew")

        self.entfernen_btn = ctk.CTkButton(master=self, text="Entfernen")
        command_func = lambda to_del=[self.label_team, self.entry_name_t, self.entry_name_g, self.entfernen_btn]: self.eingabe_weiteres_team_loeaschen(to_del)
        self.entfernen_btn.configure(command= command_func)
        if len(self.entrys) > 0:
            self.entfernen_btn.grid(row=self.team_row, column=3, padx=(10,30), pady=0, sticky="ew")

        entry_row = (self.entry_name_t, self.entry_name_g, self.entfernen_btn)
        self.entrys.append(entry_row)

        self.weiteres_team_btn.grid(row=self.team_row+1, column=0, padx=(50,50), pady=20, sticky="ew", columnspan=4)

    def eingabe_weiteres_team_loeaschen(self, felder):
        if len(self.entrys) > 1:
            self.entrys.pop()
            self.entrys[-1][2].configure(state="enabeld")
            felder[0].destroy()
            felder[1].destroy()
            felder[2].destroy()
            felder[3].destroy()
            self.team_row -= 1
            self.weiteres_team_btn.grid(row=self.team_row+1, column=0, padx=(50,50), pady=20, sticky="ew", columnspan=4)


class GruppenFrame(ctk.CTkFrame):
    """
    Frame in denen das Eintragen der Runden durchgeführt wird
    """
    def __init__(self, master, gruppe_der_runde, gruppen_lokal, runden_lokal, name_gruppe, turniername, teams_lokal):
        super().__init__(master)
        self.row_der_spiele = 0

        self.tabelle_aufbauen(gruppen_lokal, name_gruppe)

        self.spiele_frame = ctk.CTkScrollableFrame(self, width=900, height=800)

        self.spiele_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.spiel_bestaetingen_liste = []

        for runde_aus_runden in runden_lokal[gruppe_der_runde]:
            self.runden_nr = ctk.CTkLabel(master=self.spiele_frame, text=f"Runde: {runde_aus_runden.rundenzahl}")
            self.runden_nr.grid(row=self.row_der_spiele, column=0, padx=(30,50), pady=10, sticky="ew", columnspan=1)
            for spiel_aus_spielen in runde_aus_runden.spiele:
                if not spiel_aus_spielen.team_1.name.startswith("-") and not spiel_aus_spielen.team_2.name.startswith("-"):
                    self.team_1 = ctk.CTkLabel(master=self.spiele_frame, text=f"{spiel_aus_spielen.team_1.name}")
                    self.team_1.grid(row=self.row_der_spiele, column=1, padx=(10,30), pady=10, sticky="e", columnspan=1)

                    self.team_1_entry = ctk.CTkEntry(master=self.spiele_frame, width=35)
                    self.team_1_entry.grid(row=self.row_der_spiele, column=2, padx=0, pady=15, sticky="ew", columnspan=1)
                    self.team_spacer = ctk.CTkLabel(master=self.spiele_frame, text=":")
                    self.team_spacer.grid(row=self.row_der_spiele, column=3, padx=(0,2), pady=15, sticky="ew", columnspan=1)
                    self.team_2_entry = ctk.CTkEntry(master=self.spiele_frame, width=35)
                    self.team_2_entry.grid(row=self.row_der_spiele, column=4, padx=0, pady=15, sticky="ew", columnspan=1)

                    self.team_2 = ctk.CTkLabel(master=self.spiele_frame, text=f"{spiel_aus_spielen.team_2.name}")
                    self.team_2.grid(row=self.row_der_spiele, column=5, padx=(30,50), pady=10, sticky="e", columnspan=1)

                    self.spiel_bestaetingen = ctk.CTkButton(master=self.spiele_frame, text="Ergebis Eintragen")

                    command_func = lambda game=spiel_aus_spielen, entrys = [self.team_1_entry, self.team_2_entry],btn=self.spiel_bestaetingen, gruppen_lokal=gruppen_lokal, name_gruppe=name_gruppe, turniername=turniername, runden_lokal=runden_lokal, teams_lokal=teams_lokal: self.spiel_eintragen(game, entrys, btn, gruppen_lokal, name_gruppe, turniername, runden_lokal, teams_lokal)

                    self.spiel_bestaetingen.configure(command=command_func)
                    self.spiel_bestaetingen.grid(row=self.row_der_spiele, column=6, padx=(30,60), pady=10, sticky="w", columnspan=1)
                    self.spiel_bestaetingen_liste.append(self.spiel_bestaetingen)

                    if spiel_aus_spielen.gespielt:
                        self.team_1_entry.insert(0,spiel_aus_spielen.ergebnis[0])
                        self.team_2_entry.insert(0,spiel_aus_spielen.ergebnis[1])
                        self.spiel_eintragen(spiel_aus_spielen, entrys=[self.team_1_entry, self.team_2_entry], btn=self.spiel_bestaetingen, gruppen_lokal=gruppen_lokal, name_gruppe=name_gruppe, turniername=turniername, runden_lokal=runden_lokal, teams_lokal=teams_lokal)

                    self.row_der_spiele += 1

        self.anpassung_der_spiele = ctk.CTkButton(self, text="Ergebnisse Anpassen", command=self.spiele_anpassen(self.spiel_bestaetingen_liste))
        self.anpassung_der_spiele.grid(row=self.row_der_spiele, column=0, padx=60, pady=10, sticky="ew", columnspan=6)

    def spiele_anpassen(self, liste_der_btn):
        for btn in liste_der_btn:
            btn.configure(state="enabled")

    def spiel_eintragen(self, spiel_aus_spielen, entrys, btn, gruppen_lokal, name_gruppe, turniername, runden_lokal, teams_lokal):
        """Eintragen eines Spieles bei Buttondruch

        Args:
            spiel_aus_spielen Spiel: Übergabe des Spiel Objektes zum Eintrag
            entrys            Entrys: Eingabefelder der Teams
        """
        ergebnis = []
        if not (spiel_aus_spielen.team_1.name.startswith("-") or spiel_aus_spielen.team_2.name.startswith("-")):
            ergebnis.append(entrys[0].get())
            ergebnis.append(entrys[1].get())
            if ergebnis[0].isdigit() and ergebnis[1].isdigit():
                spiel_aus_spielen.ergebnis_eintragen(int(ergebnis[0]), int(ergebnis[1]))
            else:
                return
        else:
            spiel_aus_spielen.gespielt = True
            spiel_aus_spielen.ergebnis = [0,0]

        entrys[0].delete(0,"end")
        entrys[1].delete(0,"end")
        entrys[0].insert(0,spiel_aus_spielen.ergebnis[0])
        entrys[1].insert(0,spiel_aus_spielen.ergebnis[1])
        btn.configure(state="disabled")
        self.tabelle_aufbauen(gruppen_lokal, name_gruppe)
        runden_json_erstellen(turniername, runden_lokal, teams_lokal)

    def tabelle_aufbauen(self, gruppen_lokal, name_gruppe):
        self.tabelle_aktuell = tabelle_erstellen(gruppen_lokal=gruppen_lokal)
        self.tabelle_der_gruppe = TabellenFrame(self, gruppe_der_runde=name_gruppe, tabelle_lokal=self.tabelle_aktuell)
        self.tabelle_der_gruppe.grid(row=0, column=1, padx=20, pady=20, sticky="n")


class TabellenFrame(ctk.CTkFrame):
    """
    Frame in denen das Eintragen der Runden durchgeführt wird
    """
    def __init__(self, master, gruppe_der_runde, tabelle_lokal):
        super().__init__(master)
        self.gruppe = ctk.CTkLabel(self, text=f"Gruppe: {gruppe_der_runde}", font=("Arial",20))
        self.gruppe.grid(row=0, column=0, padx=50, pady=10, sticky="ew", columnspan=4)
        self.titel_team = ctk.CTkLabel(self, text="Team")
        self.titel_team.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.titel_punkte = ctk.CTkLabel(self, text="Punkte")
        self.titel_punkte.grid(row=1, column=2, padx=20, pady=10, sticky="ew")
        self.titel_diff = ctk.CTkLabel(self, text="Diff")
        self.titel_diff.grid(row=1, column=3, padx=20, pady=10, sticky="ew")

        index_position = 1
        for team_in_gruppe, team_stats in tabelle_lokal[gruppe_der_runde].items():
            if not team_in_gruppe.startswith("-"):
                self.position = ctk.CTkLabel(self, text=f"{index_position}.")
                index_position += 1
                self.position.grid(row=index_position, column=0, padx=20, pady=10, sticky="ew")
                self.team = ctk.CTkLabel(self, text=team_in_gruppe)
                self.team.grid(row=index_position, column=1, padx=20, pady=10, sticky="ew")
                self.punkte_des_teams = ctk.CTkLabel(self, text=team_stats['punkte'])
                self.punkte_des_teams.grid(row=index_position, column=2, padx=20, pady=10, sticky="ew")
                self.treffer_diff = ctk.CTkLabel(self, text=team_stats['treffer_diff'])
                self.treffer_diff.grid(row=index_position, column=3, padx=20, pady=10, sticky="ew")


class MainFrame(ctk.CTkFrame):
    """
    Main  frame in dem Spiele eingetragen werden können und die Tabelle dargestellt wird
    """
    def __init__(self, master, teams_lokal, gruppen_lokal, runden_lokal, turniername):
        super().__init__(master)
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=10, pady=0, sticky="")


        self.gruppencounter = 0
        for gruppe_aus_gruppen in gruppen_lokal:
            self.tabview.add(f"Gruppe {gruppe_aus_gruppen.name}")
            self.tabview.tab(f"Gruppe {gruppe_aus_gruppen.name}").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

            self.gruppen_frame = GruppenFrame(self.tabview.tab(f"Gruppe {gruppe_aus_gruppen.name}"), gruppe_der_runde=self.gruppencounter, gruppen_lokal=gruppen_lokal, runden_lokal=runden_lokal, name_gruppe=gruppe_aus_gruppen.name, turniername=turniername, teams_lokal=teams_lokal)
            self.gruppen_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

            self.gruppencounter += 1

#----- Zusammenführung der Frames für das GUI und Handhabung des Ablaufs -----#
class App(ctk.CTk):
    """
    Zusammenführung der Frames für das GUI und Handhabung des Ablaufs
    """
    def __init__(self):
        super().__init__()
        if not os.path.isdir("turniere"):
            os.mkdir("turniere")
        #generelles Setup für das Gui
        self.title('Turnierplaner')
        self.geometry("1280x1300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #erstellen des Willkommen Frames
        self.willkommen_frame = WillkommenFrame(self)
        self.willkommen_frame.grid(row=0, column=0, padx=10, pady=10, sticky="")

        self.live_frame = self.willkommen_frame

        self.fenster_steuerung = ctk.CTkButton(self, text="Lade Turnier", command=lambda: self.fenster_aendern(self.live_frame))
        self.fenster_steuerung.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="n")

        #deklaration der Variablen für den Ablauf
        self.teams = []
        self.gruppen = []
        self.runden = []
        self.turniername = None
        self.aktueller_status = "Generiert"

    def fenster_aendern(self, frame):
        """
        schließen des Aktuellen Frames und öffnen neuer Frames, abhängig vom Status
        """
        if not self.turniername:
            self.turniername = self.willkommen_frame.entry_turnier.get()
            print(self.turniername)
            if self.turniername != "" and not self.turniername.isspace() and self.turniername.isprintable():
                frame.destroy()
                if not os.path.isdir(f"turniere/{self.turniername}"):
                    os.mkdir(f"turniere/{self.turniername}")
            else:
                self.turniername = None
                return

        if self.aktueller_status == "Generiert":
            self.teams, self.gruppen = turnier_setup(self.turniername, self.aktueller_status, self.live_frame)
            if not self.teams:
                self.aktueller_status = "Turnier_Setup_neuanlage"
                #erstellen des Team/Gruppen Erstell Frames
                self.team_erstellen_frame = TeamErstellenFrame(self)
                self.team_erstellen_frame.grid(row=0, column=0, padx=10, pady=10, sticky="")
                self.live_frame = self.team_erstellen_frame
                self.close.configure(text="Bestätigen der Anlage")
            else:
                self.aktueller_status = "Turnier_Setup_angelegt"
        elif self.aktueller_status == "Turnier_Setup_neuanlage":
            self.teams, self.gruppen = turnier_setup(self.turniername, self.aktueller_status, self.live_frame)
            self.aktueller_status = "Turnier_Setup_angelegt"

        if self.aktueller_status == "Turnier_Setup_angelegt":
            if os.path.isfile(f"turniere/{self.turniername}/runden.json"):
                self.runden, self.runden_sind_eingetragen = runden_daten_aus_json(self.turniername, self.teams, self.gruppen)
            else:
                self.runden, self.runden_sind_eingetragen = spielplan_erstellen(self.turniername, self.teams, self.gruppen)

            self.main_frame = MainFrame(self, self.teams, self.gruppen, self.runden, self.turniername)
            self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="")


app = App()
app.mainloop()
