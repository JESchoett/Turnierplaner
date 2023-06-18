import pandas as pd

data_gruppen_json = pd.read_json("turniere/Streetball2023/gruppen.json")
for column in data_gruppen_json:
    for _, team_data in data_gruppen_json[column].items():
        print(team_data["name"])