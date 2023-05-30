class Spiel():
    def __init__(self, paar, t1, t2, nr, gespielt):
        self.paar = paar
        self.t1 = t1
        self.t2 = t2
        self.runde = nr
        self.gespielt = gespielt
        self.ergebnis =[0,0]

    def punkteVergabe(self, t1P, t2P):
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


    def ergebnisEintragen(self, t1P, t2P):
        if self.t1.name != "-" and self.t2.name != "-":
            self.ergebnis[0] = t1P
            self.ergebnis[1] = t2P
            self.punkteVergabe(self, t1P, t2P)

        self.gespielt = True
        return self

    def ergebnisAusCSV(self):
        if self.t1.name != "-" and self.t2.name != "-":
            t1P = self.ergebnis[0]
            t2P = self.ergebnis[1]
            self.punkteVergabe(self, t1P, t2P)
            return self
