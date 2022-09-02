#import requests

api_key = "3eee17d68d92449198eddf0d37bc1d2f"

class DataItem():

    def __init__(self, week, away_team, home_team, spread):
        self.week = week
        self.away_team = away_team
        self.home_team = home_team
        self.spread = spread
        
    def get_favorite(self):
        if self.spread < 0:
            return self.home_team
        else:
            return self.away_team
            
    def get_underdog(self):
        if self.spread < 0:
            return self.away_team
        else:
            return self.home_team
            
    def to_string(self):
        return "{},{},{},{}".format(self.week, self.away_team, self.home_team, self.spread)

import json

schedule_data = ""

with open("season_data_2022.json", "r") as infile:
    for line in infile:
        schedule_data += line
        
season_data = json.loads(schedule_data)

print(season_data[0])

with open("season_data_2022.csv", "w") as outfile:
    outfile.write("Week,AwayTeam,HomeTeam,Spread\n")
    for data_item in season_data:
        item = DataItem(data_item["Week"], data_item["AwayTeam"], data_item["HomeTeam"], data_item["PointSpread"])
        outfile.write(item.to_string() + "\n")