"""
Deklaration der Klasse Spiel
"""
from team import Team

class Spiel:
    """
    Klasse die die Daten eines Spieles speichert
    """
    def __init__(self, paar=str, team_1=Team, team_2=Team, runde=int, gespielt=bool, ergebnis=list):
        self.paar = paar
        self.team_1 = team_1
        self.team_2 = team_2
        self.runde = runde
        self.gespielt = gespielt
        self.ergebnis = ergebnis


    def ergebnis_eintragen(self, team_1_punkte, team_2_punkte):
        """
        Übergabe des Ergebnises an die punkte_vergabe aus dem Life Programm
        """
        self.ergebnis[0] = team_1_punkte
        self.ergebnis[1] = team_2_punkte

        if team_1_punkte > team_2_punkte:
            self.team_1.punkte += 3
        elif team_1_punkte < team_2_punkte:
            self.team_2.punkte += 3
        else:
            self.team_1.punkte += 1
            self.team_2.punkte += 1

        self.team_1.treffer       += team_1_punkte
        self.team_1.gegentreffer  += team_2_punkte

        self.team_2.treffer       += team_2_punkte
        self.team_2.gegentreffer  += team_1_punkte

        self.gespielt = True
        return self
