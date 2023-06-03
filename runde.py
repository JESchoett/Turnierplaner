"""
Deklaration der Klasse Runde
"""
class Runde():
    """
    Klasse die alle Spiele einer Runde speichert
    """
    def __init__(self, rundenzahl, spiele, runde_gespielt, gruppe_der_runde):
        self.rundenzahl = rundenzahl
        self.spiele = spiele
        self.runde_gespielt = runde_gespielt
        self.gruppe_der_runde = gruppe_der_runde
