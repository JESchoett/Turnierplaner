"""
Aktuell store ich hier die Design Idee, bevor ich in main.py
das Design mit den Funktionalitäten des Skriptes zusammenbringe
"""
import os
import random
import pandas
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

    def gruppen_anlage(teams_lokal, gruppen_lokal, gruppen_in_turnier, live_frame):
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
                            spiele_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)
                        eingabe_erkannt = True
                    elif engabe_dialog.lower().startswith("h"):
                        spiele_werden_gespielt = anzahl_der_teams/2*(anzahl_der_teams-1)
                        eingabe_erkannt = True
                    elif engabe_dialog.lower().startswith("r"):
                        spiele_werden_gespielt = anzahl_der_teams*(anzahl_der_teams-1)
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
        data_gruppen_json = pandas.read_json(f"turniere/{turniername}/gruppen.json")
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
        teams_lokal, gruppen_lokal = gruppen_anlage(teams_lokal, gruppen_lokal, gruppen_in_turnier, live_frame)
    else:
        if status_anlage == "Turnier_Setup_neuanlage":
            for team_name, team_gruppe, ent_button in live_frame.entrys:
                teams_lokal.append(Team(name=team_name.get(), gruppe=team_gruppe.get(),punkte=0,treffer=0,gegentreffer=0))

            #anlage der Grupen.json
            dataframe = pandas.DataFrame(data=teams_lokal)
            dataframe.to_json(f"turniere/{turniername}/gruppen.json")

            teams_lokal, gruppen_lokal = gruppen_anlage(teams_lokal, gruppen_lokal, gruppen_in_turnier, live_frame)

        return teams_lokal, gruppen_lokal


#----- Erstellung der Frames für das GUI -----#
class WillkommenFrame(ctk.CTkFrame):
    """Erstellen eines Frames zum Laden des Turnieres"""
    def __init__(self, master):
        super().__init__(master)

        self.listiner = 0
        self.label_welc = ctk.CTkLabel(self, text="Willkommen beim Turnierplaner", font=("Arial",30))
        self.label_welc.grid(row=0, column=0, padx=30, pady=(30,10), sticky="ew", columnspan=100)

        self.label_2 = ctk.CTkLabel(self, text="Bitte Turniernamen eingeben: ", font=("Arial",15))
        self.label_2.grid(row=1, column=0, padx=10, pady=0, sticky="e")

        self.entry_turnier = ctk.CTkEntry(self, width=250)
        self.entry_turnier.grid(row=1, column=1, padx=10, pady=(20,30), sticky="w", columnspan=100)

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


class TeamErstellen(ctk.CTkFrame):
    """
    Erstellen eines Frames in dem Teams und Gruppen angelegt werden
    Außerdem wird die gruppen.json hier angelegt
    """
    def __init__(self, master):
        super().__init__(master)

        self.label_welc = ctk.CTkLabel(self, text="Anlage von Teams und Gruppen", font=("Arial",30))
        self.label_welc.grid(row=0, column=0, padx=(30,10), pady=(30,10), sticky="e", columnspan=4)

        self.button_t = ctk.CTkButton(self, text="Team")
        self.button_t.grid(row=1, column=1, padx=(50,0), pady=(10, 0), sticky="ew")

        self.button_g = ctk.CTkButton(self, text="Gruppe")
        self.button_g.grid(row=1, column=2, padx=(0,10), pady=(10, 0), sticky="ew")

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
        #entry_name_t = "entry_team" + str(self.team_row)
        #entry_name_g = "entry_gruppe" + str(self.team_row)

        self.label_team.grid(row=self.team_row, column=0, padx=0, pady=0, sticky="e")

        self.entry_name_t = ctk.CTkEntry(self, width=10)
        self.entry_name_t.grid(row=self.team_row, column=1, padx=(50,0), pady=0, sticky="ew")

        self.entry_name_g = ctk.CTkEntry(self, width=30)
        self.entry_name_g.grid(row=self.team_row, column=2, padx=(0,10), pady=0, sticky="ew")

        self.entfernen_btn = ctk.CTkButton(master=self, text="Entfernen")
        command_func = lambda to_del=[self.label_team, self.entry_name_t, self.entry_name_g, self.entfernen_btn]: self.eingabe_weiteres_team_loeaschen(to_del)
        self.entfernen_btn.configure(command= command_func)
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
        self.geometry("1000x800")
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
                os.mkdir(f"turniere/{self.turniername}")
            else:
                self.turniername = None
                return

        if self.aktueller_status == "Generiert":
            self.teams, self.gruppen = turnier_setup(self.turniername, self.aktueller_status, self.live_frame)
            if not self.teams:
                self.aktueller_status = "Turnier_Setup_neuanlage"
                #erstellen des Team/Gruppen Erstell Frames
                self.team_erstellen_frame = TeamErstellen(self)
                self.team_erstellen_frame.grid(row=0, column=0, padx=10, pady=10, sticky="")
                self.live_frame = self.team_erstellen_frame
                self.close.configure(text="Bestätigen der Anlage")
            else:
                self.aktueller_status = "Turnier_Setup_angelegt"
        elif self.aktueller_status == "Turnier_Setup_neuanlage":
            self.teams, self.gruppen = turnier_setup(self.turniername, self.aktueller_status, self.live_frame)


app = App()
app.mainloop()
