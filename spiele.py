"""
Deklaration der Klasse Spiel
"""

class Spiel():
    """
    Klasse die die Daten eines Spieles speichert
    """
    def __init__(self, paar, team_1, team_2, runde, gespielt):
        self.paar = paar
        self.team_1 = team_1
        self.team_2 = team_2
        self.runde = runde
        self.gespielt = gespielt
        self.ergebnis =[0,0]

    def punkte_vergabe(self, team_1_punkte, team_2_punkte):
        """
        Vergabe von Punkten an Teams
        Pflege der Tor Verhältnisse
        """

        if team_1_punkte > team_2_punkte:
            self.team_1.punkte += 3
        if team_1_punkte < team_2_punkte:
            self.team_2.punkte += 3
        if team_1_punkte == team_2_punkte:
            self.team_1.punkte += 1
            self.team_2.punkte += 1

        self.team_1.treffer += team_1_punkte
        self.team_1.gegentreffer  += team_2_punkte
        self.team_2.treffer += team_2_punkte
        self.team_2.gegentreffer  += team_1_punkte


    def ergebnis_eintragen(self, team_1_punkte, team_2_punkte):
        """
        Übergabe des Ergebnises an die punkte_vergabe aus dem Life Programm
        """
        if self.team_1.name != "-" and self.team_2.name != "-":
            self.ergebnis[0] = team_1_punkte
            self.ergebnis[1] = team_2_punkte
            self.punkte_vergabe(team_1_punkte, team_2_punkte)

        self.gespielt = True
        return self

    def ergebnis_aus_csv(self):
        """
        Übergabe des Ergebnises an die punkte_vergabe vom Setup aus der CSV
        """
        if self.team_1.name != "-" and self.team_2.name != "-":
            team_1_punkte = self.ergebnis[0]
            team_2_punkte = self.ergebnis[1]
            self.punkte_vergabe(team_1_punkte, team_2_punkte)
            return self
