"""
Deklaration der Klasse Gruppe
"""
class Gruppe():
    """
    Gruppe die alle Teams einer Gruppe speichert
    """
    def __init__(self, name, spieleanzahl, teams_in_gruppe):
        self.name = name
        self.spieleanzahl = spieleanzahl
        self.teams_in_gruppe = teams_in_gruppe

    def teams_aendern(self, neue_teams):
        """
        Nachträgliche Anpassung der Teams in der Gruppe
        """
        self.teams_in_gruppe = neue_teams
