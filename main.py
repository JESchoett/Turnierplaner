import pandas
import os

from team import Team

print("Willkommen beim Turnierplaner")

if not os.path.isdir("turniere"):
    os.mkdir("turniere")

turniername = input("Turniername angeben: ")

if os.path.isdir(f"turniere/{turniername}"):
    data = pandas.read_csv(f"turniere/{turniername}/gruppen.csv")
    print("turnier wurde gefunden")
    print(data)
else:
    print("kein turnier gefunden... ein neues turnier wird angelegt")
    os.mkdir(f"turniere/{turniername}")

    teams = []
    def neuesTeam(teamName, teamGruppe):
        t = Team(name = teamName, gruppe=teamGruppe)
        return t

    teamAnlegen = True
    while teamAnlegen:
        weitereAnlage = input("möchtest du ein neues Team Anlegen? (J/N): ")
        if  weitereAnlage == "N" or weitereAnlage == "n":
            teamAnlegen = False
        else:
            teamName = input("Team Name angeben: ")
            teamGruppe = input("in welcher Gruppe soll das Team Spielen?: ")
            teams.append(neuesTeam(teamName, teamGruppe))

    teamsDict = {
        "teams": [t.name for t in teams],
        "gruppe": [t.gruppe for t in teams]
    }
    df = pandas.DataFrame(teamsDict)
    df.to_csv(f"turniere/{turniername}/gruppen.csv")