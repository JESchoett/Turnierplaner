class Team():
    def __init__(self, name, gruppe, score = 0, pointsScored = 0, pointsTaken = 0):
        self.name = name
        self.gruppe = gruppe
        self.score = score
        self.pointsScored = pointsScored
        self.pointsTaken = pointsTaken

    def gruppeAendern(self, neueGruppe):
        self.gruppe = neueGruppe