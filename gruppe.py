class Gruppe():
    def __init__(self, name, spieleanzahl, teamsInGruppe):
        self.name = name
        self.spieleanzahl = spieleanzahl
        self.teamsInGruppe = teamsInGruppe

    def teamsAendern(self, neueTeams):
        self.teamsInGruppe = neueTeams