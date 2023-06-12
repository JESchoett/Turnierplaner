"""
Deklaration der Klasse Runde
"""
class Runde:
    """
    Klasse die alle Spiele einer Runde speichert
    """
    def __init__(self, rundenzahl=int, spiele=list, runde_gespielt=bool, gruppe_der_runde=str):
        self.rundenzahl = rundenzahl
        self.spiele = spiele
        self.runde_gespielt = runde_gespielt
        self.gruppe_der_runde = gruppe_der_runde
