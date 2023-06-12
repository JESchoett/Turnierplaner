"""
Deklaration der Klasse Team
"""
from typing import Union
from gruppe import Gruppe

class Team:
    """
    Klasse die die Daten eines Teams speichert
    """
    def __init__(self, name=str, gruppe=Union[str, Gruppe], punkte = int, treffer = int, gegentreffer = int):
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
