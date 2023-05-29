class Team():
    def __init__(self, name, gruppe, punkte = 0, toreScored = 0, toreTaken = 0):
        self.name = name
        self.gruppe = gruppe
        self.punkte = punkte
        self.toreScored = toreScored
        self.toreTaken = toreTaken

    def gruppeAendern(self, neueGruppe):
        self.gruppe = neueGruppe