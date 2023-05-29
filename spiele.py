class Spiel():
    def __init__(self, paar, t1, t2, nr):
        self.paar = paar
        self.t1 = t1
        self.t2 = t2
        self.runde = nr
        self.gespielt = False

    def ergebnisEintragen(self, t1P, t2P):
        if self.t1.name != "-" and self.t2.name != "-":
            if t1P > t2P:
                self.t1.punkte += 3
            if t1P < t2P:
                self.t2.punkte += 3
            if t1P == t2P:
                self.t1.punkte += 1
                self.t2.punkte += 1

            self.t1.pointsScored += t1P
            self.t1.pointsTaken  += t2P
            self.t2.pointsScored += t2P
            self.t2.pointsTaken  += t1P

        self.gespielt = True