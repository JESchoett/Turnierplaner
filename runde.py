"""
Deklaration der Klasse Runde
"""
from dataclasses import dataclass

@dataclass
class Runde:
    """
    Klasse die alle Spiele einer Runde speichert
    """
    rundenzahl: int
    spiele: list
    runde_gespielt: bool
    gruppe_der_runde: str
