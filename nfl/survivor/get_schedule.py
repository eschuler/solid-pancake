#import requests
import json

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
        
def get_favorite(away_team, home_team, point_spread):
    if point_spread < 0:
        return home_team
    elif point_spread > 0:
        return away_team
    else:
        print("Tied point spread! {} @ {}: {}".format(away_team, home_team, point_spread))

schedule_data = ""

with open("season_data_2022.json", "r") as infile:
    for line in infile:
        schedule_data += line
        
season_data = json.loads(schedule_data)

print(season_data[0])

season_data_array = {}

biggest_wins_per_team = {}
biggest_wins_per_week = {}

with open("season_data_2022.csv", "w") as outfile:
    outfile.write("Week,AwayTeam,HomeTeam,Spread\n")
    
    for data_item in season_data:
    
        item = DataItem(data_item["Week"], data_item["AwayTeam"], data_item["HomeTeam"], data_item["PointSpread"])
        outfile.write(item.to_string() + "\n")
        
        if data_item["Week"] not in season_data_array.keys():
            season_data_array[data_item["Week"]] = {}
            
        if data_item["Week"] not in biggest_wins_per_week.keys():
            biggest_wins_per_week[data_item["Week"]] = ("Foo", 0)