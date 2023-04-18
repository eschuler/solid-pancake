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

unique_teams = [
    'ARI', 'ATL', 'BAL', 'BUF', 
    'CAR', 'CHI', 'CIN', 'CLE', 
    'DAL', 'DEN', 'DET', 'GB', 
    'HOU', 'IND', 'JAX', 'KC', 
    'LAC', 'LAR', 'LV',  'MIA', 
    'MIN', 'NE',  'NO',  'NYG', 
    'NYJ', 'PHI', 'PIT', 'SEA', 
    'SF',  'TB',  'TEN', 'WAS']
     
team_idx = {}
for i in range(len(unique_teams)):
    team_idx[unique_teams[i]] = i
    
print(team_idx)

nfl_grid = [];
num_weeks_in_season = 18;
for i in range(len(unique_teams)):
    new_row = []
    for j in range(num_weeks_in_season):
        new_row.append(("", 0.0))
    nfl_grid.append(new_row)

for data_item in season_data:

    # tuple item 1
    home_team     = data_item["HomeTeam"]
    home_team_idx = team_idx[home_team]
    
    # tuple item 2
    spread = data_item["PointSpread"]

    # row idx
    away_team     = data_item["AwayTeam"]
    if away_team == "BYE":
        nfl_grid[away_team_idx][week_idx] = ("BYE", 0.0)
        continue
    away_team_idx = team_idx[away_team]
    
    # col idx    
    week = data_item["Week"]
    week_idx = week - 1
    
    #print("nfl_grid[{}][{}] = ({}, {})".format(away_team_idx, week, home_team, spread))
    
    nfl_grid[away_team_idx][week_idx] = ("@ " + home_team,  spread)
    nfl_grid[home_team_idx][week_idx] = ("vs " + away_team, spread * -1)
    
#print(nfl_grid)

for i in range(num_weeks_in_season):
    week_matchups = []
    print("\nWeek {} Matchups:".format(i + 1))
    for j in range(len(unique_teams)):
        week_matchups.append((unique_teams[j], nfl_grid[j][i][1], nfl_grid[j][i][0]))
    week_matchups = sorted(week_matchups, key=lambda matchup: matchup[1], reverse=True)
    for m in week_matchups[:10]:
        print("    {} {} - {}".format(m[0], m[2], m[1]))
    print()
    #break

exit(0)

with open("season_grid_2022.csv", "w") as outfile:
    outfile.write("AwayTeam\Week")
    
    # write top header
    for i in range(num_weeks_in_season):
        outfile.write(",{}".format(i + 1))
    outfile.write("\n")
        
    # write each row    
    for i in range(len(unique_teams)):
        # write left column header
        outfile.write("{}".format(unique_teams[i]))
        
        # write each column value
        for j in range(num_weeks_in_season):
            curr_tuple = nfl_grid[i][j]
            outfile.write(",\"{}, {}\"".format(curr_tuple[0], curr_tuple[1]))
        outfile.write("\n")
    
exit(1)

with open("season_data_2022.csv", "w") as outfile:
    outfile.write("Week,AwayTeam,HomeTeam,Spread\n")
    
    for data_item in season_data:
        
        week = data_item["Week"]
    
        item = DataItem(week, data_item["AwayTeam"], data_item["HomeTeam"], data_item["PointSpread"])
        outfile.write(item.to_string() + "\n")
        
        if week not in season_data_array.keys():
            season_data_array[data_item["Week"]] = {}
            
        if week not in biggest_wins_per_week.keys():
            biggest_wins_per_week[week] = ("Foo", 0)
            
        if week == 1:
            if data_item["AwayTeam"] not in unique_teams:
                unique_teams.append(data_item["AwayTeam"])
            if data_item["HomeTeam"] not in unique_teams:
                unique_teams.append(data_item["HomeTeam"])
                
unique_teams = sorted(unique_teams)
print(unique_teams)
#print(len(unique_teams))