"""
unittest alle funktionen des Turnierplaners
damit dieser Test erfolgreich funktioniert muss in dem Ordner
"""
import os
import unittest
from unittest.mock import patch

from team import Team
from gruppe import Gruppe
from spiele import Spiel
from runde import Runde

from main import welcome, neues_team, neue_gruppe, neue_runde, neues_spiel, turnier_setup, gruppen_anlage, spielplan_erstellen, runden_daten_aus_json, spiel_eintragen

class Test_neue_Objekte_erstellung(unittest.TestCase):
    def test_welcome(self):
        with patch('builtins.print') as mocked_print:
            welcome()
            mocked_print.assert_called_with("Willkommen beim Turnierplaner")

    def test_neues_team(self):
        team = neues_team("Team A", "Gruppe 1")
        self.assertIsInstance(team, Team)
        self.assertEqual(team.name, "Team A")
        self.assertEqual(team.gruppe, "Gruppe 1")

    def test_neue_gruppe(self):
        gruppe = neue_gruppe("Gruppe 1", 5, [])
        self.assertIsInstance(gruppe, Gruppe)
        self.assertEqual(gruppe.name, "Gruppe 1")
        self.assertEqual(gruppe.spieleanzahl, 5)
        self.assertEqual(gruppe.teams_in_gruppe, [])

    def test_neue_runde(self):
        runde = neue_runde(1, [], False, "Gruppe 1")
        self.assertIsInstance(runde, Runde)
        self.assertEqual(runde.rundenzahl, 1)
        self.assertEqual(runde.spiele, [])
        self.assertFalse(runde.runde_gespielt)
        self.assertEqual(runde.gruppe_der_runde, "Gruppe 1")

    def test_neues_spiel(self):
        spiel = neues_spiel("Team A/Team B", Team("Team A", "Gruppe 1"), Team("Team B", "Gruppe 1"), 1, False, [0, 0])
        self.assertIsInstance(spiel, Spiel)
        self.assertEqual(spiel.paar, "Team A/Team B")
        self.assertIsInstance(spiel.team_1, Team)
        self.assertEqual(spiel.team_1.name, "Team A")
        self.assertIsInstance(spiel.team_2, Team)
        self.assertEqual(spiel.team_2.name, "Team B")
        self.assertEqual(spiel.runde, 1)
        self.assertFalse(spiel.gespielt)
        self.assertEqual(spiel.ergebnis, [0, 0])

class Test_Teams_aus_turnier_setup(unittest.TestCase):
    @patch('builtins.input', side_effect=['Test-Turnier', 'n'])
    def test_turnier_setup_existing_json(self, mock_input):
        # Erstellen einer vorhandenen JSON-Datei für den Test
        json_content = """
        {
            "Gruppe A": {
                "team1": {
                    "name": "Team 1",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team2": {
                    "name": "Team 2",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                }
            }
        }
        """
        with open("turniere/Test-Turnier/gruppen.json", "w") as json_file:
            json_file.write(json_content)

        # Ausführen der Funktion turnier_setup
        turniername, teams_lokal = turnier_setup()

        # Überprüfen der Rückgabewerte
        self.assertEqual(turniername, 'Test-Turnier')
        self.assertEqual(len(teams_lokal), 2)

        os.remove("turniere/Test-Turnier/gruppen.json")


    @patch('builtins.input', side_effect=['Test-Turnier', 'y', 'Team 1', 'A', 'y', 'n'])
    def test_turnier_setup_eingabe_Team_und_Gruppe(self, mock_input):
        # Ausführen der Funktion turnier_setup
        turniername, teams_lokal = turnier_setup()

        # Überprüfen der Rückgabewerte
        self.assertEqual(turniername, 'Test-Turnier')
        self.assertEqual(len(teams_lokal), 1)

        os.remove("turniere/Test-Turnier/gruppen.json")

    @patch('builtins.input', side_effect=['Test-Turnier', 'y', 'Team 1', '', 'y', 'n'])
    def test_turnier_setup_eingabe_Team_und_Gruppe_empty_group(self, mock_input):
        # Ausführen der Funktion turnier_setup
        turniername, teams_lokal = turnier_setup()

        # Überprüfen der Rückgabewerte
        self.assertEqual(turniername, 'Test-Turnier')
        self.assertEqual(len(teams_lokal), 1)

        os.remove("turniere/Test-Turnier/gruppen.json")

class Test_GruppenTeams_aus_gruppen_anlage(unittest.TestCase):
    def setUp(self):
        # Create a patch for 'builtins.input'
        self.mock_input = patch('builtins.input', side_effect=['Test-Turnier', 'n'])
        # Start the patch
        self.mock_input.start()
        # Call the common setup method
        self.common_setup()

    def tearDown(self):
        # Stop the patch
        self.mock_input.stop()
        os.remove("turniere/Test-Turnier/gruppen.json")

    def common_setup(self):
        # Erstellen einer vorhandenen JSON-Datei für den Test
        json_content = """
        {
            "A": {
                "team1": {
                    "name": "Team 1",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team2": {
                    "name": "Team 2",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team3": {
                    "name": "Team 3",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team4": {
                    "name": "Team 4",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                }
            }
        }
        """
        with open("turniere/Test-Turnier/gruppen.json", "w") as json_file:
            json_file.write(json_content)

        self.turniername, self.teams_lokal = turnier_setup()

    @patch('builtins.input', side_effect=['h'])
    def test_turnier_setup_eingabe_hinrunde(self, mock_input):
        gruppen_lokal, teams_lokal = gruppen_anlage(self.turniername, self.teams_lokal)

        self.assertEqual(len(gruppen_lokal), 1)
        self.assertEqual(gruppen_lokal[0].name, "A")
        self.assertEqual(gruppen_lokal[0].spieleanzahl, 6)
        self.assertEqual(len(gruppen_lokal[0].teams_in_gruppe), 4)

    @patch('builtins.input', side_effect=['r'])
    def test_turnier_setup_eingabe_hin_und_rueckrunde(self, mock_input):
        gruppen_lokal, teams_lokal = gruppen_anlage(self.turniername, self.teams_lokal)

        self.assertEqual(len(gruppen_lokal), 1)
        self.assertEqual(gruppen_lokal[0].name, "A")
        self.assertEqual(gruppen_lokal[0].spieleanzahl, 12)
        self.assertEqual(len(gruppen_lokal[0].teams_in_gruppe), 4)

    @patch('builtins.input', side_effect=['9'])
    def test_turnier_setup_eingabe_runden_num(self, mock_input):
        gruppen_lokal, teams_lokal = gruppen_anlage(self.turniername, self.teams_lokal)

        self.assertEqual(len(gruppen_lokal), 1)
        self.assertEqual(gruppen_lokal[0].name, "A")
        self.assertEqual(gruppen_lokal[0].spieleanzahl, 9)
        self.assertEqual(len(gruppen_lokal[0].teams_in_gruppe), 4)

class Test_Runden_aus_spielplan_erstellen(unittest.TestCase):
    def setUp(self):
        # Create a patch for 'builtins.input'
        self.mock_input = patch('builtins.input', side_effect=['Test-Turnier', 'n', 'r'])
        # Start the patch
        self.mock_input.start()
        # Call the common setup method
        self.common_setup()

    def tearDown(self):
        # Stop the patch
        self.mock_input.stop()
        os.remove("turniere/Test-Turnier/gruppen.json")

    def common_setup(self):
        # Erstellen einer vorhandenen JSON-Datei für den Test
        json_content = """
        {
            "A": {
                "team1": {
                    "name": "Team 1",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team2": {
                    "name": "Team 2",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team3": {
                    "name": "Team 3",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team4": {
                    "name": "Team 4",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                }
            }
        }
        """
        with open("turniere/Test-Turnier/gruppen.json", "w") as json_file:
            json_file.write(json_content)

        # Ausführen der Funktion turnier_setup
        self.turniername, self.teams_lokal = turnier_setup()
        self.gruppen_lokal, self.teams_lokal = gruppen_anlage(self.turniername, self.teams_lokal)

    def test_erstellung_der_runden(self):
        runden_lokal, runden_sind_eingetragen = spielplan_erstellen(self.turniername, self.teams_lokal, self.gruppen_lokal)

        self.assertEqual(len(runden_lokal[0]), 6)
        self.assertEqual(runden_lokal[0][0].rundenzahl, 1)
        self.assertEqual(runden_lokal[0][0].spiele[0].runde, 1)

        self.assertEqual(runden_sind_eingetragen['A']['runde_eintragen'], 0)
        self.assertEqual(runden_sind_eingetragen['A']['max_runden'], 6)

class Test_Runden_aus_runden_daten_aus_json(unittest.TestCase):
    def setUp(self):
        # Create a patch for 'builtins.input'
        self.mock_input = patch('builtins.input', side_effect=['Test-Turnier', 'n'])
        # Start the patch
        self.mock_input.start()
        # Call the common setup method
        self.common_setup()

    def tearDown(self):
        # Stop the patch
        self.mock_input.stop()
        os.remove("turniere/Test-Turnier/gruppen.json")
        os.remove("turniere/Test-Turnier/runden.json")

    def common_setup(self):
        # Erstellen einer vorhandenen JSON-Datei für den turnier_setup
        json_content = """
        {
            "A": {
                "team1": {
                    "name": "Team 1",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team2": {
                    "name": "Team 2",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team3": {
                    "name": "Team 3",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team4": {
                    "name": "Team 4",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                }
            }
        }
        """
        with open("turniere/Test-Turnier/gruppen.json", "w") as json_file:
            json_file.write(json_content)

        self.turniername, self.teams_lokal = turnier_setup()

        # Erstellen einer vorhandenen JSON-Datei für den gruppen_anlage
        json_content = """
        {
          "0": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 1,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 2/Team 3",
                  "runde": 1,
                  "team_1": "Team 2",
                  "team_2": "Team 3"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 4/Team 1",
                  "runde": 1,
                  "team_1": "Team 4",
                  "team_2": "Team 1"
                }
              ]
            }
          },
          "1": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 2,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 2/Team 4",
                  "runde": 2,
                  "team_1": "Team 2",
                  "team_2": "Team 4"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 3/Team 1",
                  "runde": 2,
                  "team_1": "Team 3",
                  "team_2": "Team 1"
                }
              ]
            }
          },
          "2": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 3,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 2/Team 1",
                  "runde": 3,
                  "team_1": "Team 2",
                  "team_2": "Team 1"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 3/Team 4",
                  "runde": 3,
                  "team_1": "Team 3",
                  "team_2": "Team 4"
                }
              ]
            }
          },
          "3": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 4,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 3/Team 2",
                  "runde": 4,
                  "team_1": "Team 3",
                  "team_2": "Team 2"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 1/Team 4",
                  "runde": 4,
                  "team_1": "Team 1",
                  "team_2": "Team 4"
                }
              ]
            }
          },
          "4": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 5,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 4/Team 2",
                  "runde": 5,
                  "team_1": "Team 4",
                  "team_2": "Team 2"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 1/Team 3",
                  "runde": 5,
                  "team_1": "Team 1",
                  "team_2": "Team 3"
                }
              ]
            }
          },
          "5": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 6,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 1/Team 2",
                  "runde": 6,
                  "team_1": "Team 1",
                  "team_2": "Team 2"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 4/Team 3",
                  "runde": 6,
                  "team_1": "Team 4",
                  "team_2": "Team 3"
                }
              ]
            }
          }
        }
        """
        with open("turniere/Test-Turnier/runden.json", "w") as json_file:
            json_file.write(json_content)

        self.gruppen_lokal, self.teams_lokal = gruppen_anlage(self.turniername, self.teams_lokal)

    def test_erstellung_der_runden_aus_json(self):
        runden_lokal, runden_sind_eingetragen = runden_daten_aus_json(self.turniername, self.teams_lokal, self.gruppen_lokal)

        self.assertEqual(len(runden_lokal[0]), 6)
        self.assertEqual(runden_lokal[0][0].rundenzahl, 1)
        self.assertEqual(runden_lokal[0][0].spiele[0].runde, 1)

        self.assertEqual(runden_sind_eingetragen['A']['runde_eintragen'], 0)
        self.assertEqual(runden_sind_eingetragen['A']['max_runden'], 6)

        spiele_counter = 0
        for runden_der_gruppe in runden_lokal[0]:
            for spiele_der_runde in runden_der_gruppe.spiele:
              spiele_counter += 1

        #es werden 6 Runden mit je 2 Spielen gespielt
        self.assertEqual(spiele_counter, 12)

class Test_spiel_eintragen(unittest.TestCase):
    def setUp(self):
        # Create a patch for 'builtins.input'
        self.mock_input = patch('builtins.input', side_effect=['Test-Turnier', 'n'])
        # Start the patch
        self.mock_input.start()
        # Call the common setup method
        self.common_setup()

    def tearDown(self):
        # Stop the patch
        self.mock_input.stop()
        os.remove("turniere/Test-Turnier/gruppen.json")
        os.remove("turniere/Test-Turnier/runden.json")

    def common_setup(self):
        # Erstellen einer vorhandenen JSON-Datei für den turnier_setup
        json_content = """
        {
            "A": {
                "team1": {
                    "name": "Team 1",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team2": {
                    "name": "Team 2",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team3": {
                    "name": "Team 3",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                },
                "team4": {
                    "name": "Team 4",
                    "gruppe": "A",
                    "punkte": 0,
                    "treffer": 0,
                    "gegentreffer": 0
                }
            }
        }
        """
        with open("turniere/Test-Turnier/gruppen.json", "w") as json_file:
            json_file.write(json_content)

        self.turniername, self.teams_lokal = turnier_setup()

        # Erstellen einer vorhandenen JSON-Datei für den gruppen_anlage
        json_content = """
        {
          "0": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 1,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 2/Team 3",
                  "runde": 1,
                  "team_1": "Team 2",
                  "team_2": "Team 3"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 4/Team 1",
                  "runde": 1,
                  "team_1": "Team 4",
                  "team_2": "Team 1"
                }
              ]
            }
          },
          "1": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 2,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 2/Team 4",
                  "runde": 2,
                  "team_1": "Team 2",
                  "team_2": "Team 4"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 3/Team 1",
                  "runde": 2,
                  "team_1": "Team 3",
                  "team_2": "Team 1"
                }
              ]
            }
          },
          "2": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 3,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 2/Team 1",
                  "runde": 3,
                  "team_1": "Team 2",
                  "team_2": "Team 1"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 3/Team 4",
                  "runde": 3,
                  "team_1": "Team 3",
                  "team_2": "Team 4"
                }
              ]
            }
          },
          "3": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 4,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 3/Team 2",
                  "runde": 4,
                  "team_1": "Team 3",
                  "team_2": "Team 2"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 1/Team 4",
                  "runde": 4,
                  "team_1": "Team 1",
                  "team_2": "Team 4"
                }
              ]
            }
          },
          "4": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 5,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 4/Team 2",
                  "runde": 5,
                  "team_1": "Team 4",
                  "team_2": "Team 2"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 1/Team 3",
                  "runde": 5,
                  "team_1": "Team 1",
                  "team_2": "Team 3"
                }
              ]
            }
          },
          "5": {
            "0": {
              "gruppe_der_runde": "A",
              "runde_gespielt": false,
              "rundenzahl": 6,
              "spiele": [
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 1/Team 2",
                  "runde": 6,
                  "team_1": "Team 1",
                  "team_2": "Team 2"
                },
                {
                  "ergebnis": [0, 0],
                  "gespielt": false,
                  "paar": "Team 4/Team 3",
                  "runde": 6,
                  "team_1": "Team 4",
                  "team_2": "Team 3"
                }
              ]
            }
          }
        }
        """
        with open("turniere/Test-Turnier/runden.json", "w") as json_file:
            json_file.write(json_content)

        self.gruppen_lokal, self.teams_lokal = gruppen_anlage(self.turniername, self.teams_lokal)
        self.runden_lokal, self.runden_sind_eingetragen = runden_daten_aus_json(self.turniername, self.teams_lokal, self.gruppen_lokal)

    @patch('builtins.input', side_effect=['0', '0', '2', '1', 'j'])
    def test_eintragen_eines_spieles(self, mock_input):
        spiel_eintragen(self.runden_sind_eingetragen, self.runden_lokal)

        #prüfung der spiel und teamdaten
        self.assertEqual(self.runden_lokal[0][0].spiele[0].gespielt, True)
        self.assertEqual(self.runden_lokal[0][0].spiele[0].team_1.punkte, 3)
        self.assertEqual(self.runden_lokal[0][0].spiele[0].team_1.treffer, 2)
        self.assertEqual(self.runden_lokal[0][0].spiele[0].team_2.punkte, 0)
        self.assertEqual(self.runden_lokal[0][0].spiele[0].team_2.treffer, 1)

    @patch('builtins.input', side_effect=['0', '0', '2', '1', 'j', '0', '1', '1', '1', 'j', 'j'])
    def test_rundenabschluss_nach_eintragen_eines_spieles(self, mock_input):
        spiel_eintragen(self.runden_sind_eingetragen, self.runden_lokal)
        spiel_eintragen(self.runden_sind_eingetragen, self.runden_lokal)

        #prüfung der spiel und teamdaten
        self.assertEqual(self.runden_lokal[0][0].spiele[1].gespielt, True)
        self.assertEqual(self.runden_lokal[0][0].spiele[1].team_1.punkte, 1)
        self.assertEqual(self.runden_lokal[0][0].spiele[1].team_1.treffer, 1)
        self.assertEqual(self.runden_lokal[0][0].spiele[1].team_2.punkte, 1)
        self.assertEqual(self.runden_lokal[0][0].spiele[1].team_2.treffer, 1)

        #prüfung des abslschlusses der runde
        self.assertEqual(self.runden_sind_eingetragen['A']["runde_eintragen"], 1)
        self.assertEqual(self.runden_lokal[0][0].runde_gespielt, True)

if __name__ == '__main__':
    unittest.main()
