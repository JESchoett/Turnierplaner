"""
Deklaration der Klasse Team
"""
from dataclasses import dataclass
from typing import Union
from gruppe import Gruppe

@dataclass
class Team:
    """
    Klasse die die Daten eines Teams speichert
    """
    name: str
    gruppe: Union[str, Gruppe]
    punkte: int
    treffer: int
    gegentreffer: int

    def gruppe_aendern(self, neue_gruppe):
        """
        Nachträgliche Anpassung der Gruppe
        """
        self.gruppe = neue_gruppe
