"""
Deklaration der Klasse Team
"""

class Team():
    """
    Klasse die die Daten eines Teams speichert
    """
    def __init__(self, name, gruppe, punkte = 0, treffer = 0, gegentreffer = 0):
        self.name = name
        self.gruppe = gruppe
        self.punkte = punkte
        self.treffer = treffer
        self.gegentreffer = gegentreffer

    def gruppe_aendern(self, neue_gruppe):
        """
        Nachträgliche Anpassung der Gruppe
        """
        self.gruppe = neue_gruppe
