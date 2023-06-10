"""
auslagerung der funktionen für die Erstellung neuer Objekte
"""
from team import Team
from gruppe import Gruppe
from spiele import Spiel
from runde import Runde

def neues_team(name_des_teams, gruppe_des_teams):
    """
    anlage eines Team Objektes
    """
    erstelltes_team = Team(name = name_des_teams, gruppe=gruppe_des_teams)
    return erstelltes_team

def neue_gruppe(name, spieleanzahl, teams_in_gruppe):
    """
    anlage eines Gruppe Objektes
    """
    erstellte_gruppe = Gruppe(name, spieleanzahl, teams_in_gruppe)
    return erstellte_gruppe

def neue_runde(rundenzahl, spiele, runde_gespielt, gruppe_der_runde):
    """
    anlage eines Runde Objektes
    """
    erstellte_runde = Runde(rundenzahl, spiele, runde_gespielt, gruppe_der_runde)
    return erstellte_runde

def neues_spiel(paar, team_1, team_2, runde, gespielt, ergebnis):
    """
    anlage eines Spiel Objektes
    """
    erstelltes_spiel = Spiel(paar, team_1, team_2, runde,gespielt, ergebnis)
    return erstelltes_spiel
