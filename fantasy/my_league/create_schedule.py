#!/usr/bin/env python

import random

# seed = Washington Super Bowls
random.seed(828791)

MIN_TEAM_ID = 1
MAX_TEAM_ID = 12

class Team:
    """
    Defines a fantasy team
    """
    
    def __init__(self, team_id, player_name):
        """
        Constructor

        :param team_id: team ID number
        :type team_id: int
        :param player_name: player name
        :type player_name: string
        """

        # error check
        if type(team_id) != int:
            raise ValueError(
                "Team ID {} is not an int ({})!".format(
                    team_id, 
                    type(team_id)
                )
            )

        # error check
        if type(player_name) != str:
            raise ValueError(
                "Player name {} is not a str ({})!".format(
                    player_name,
                    type(player_name)
                )
            )

        # error check
        if len(player_name) == 0:
            raise ValueError("Player name cannot be blank!")

        # error check
        if team_id < MIN_TEAM_ID or team_id > MAX_TEAM_ID:
            raise ValueError(
                "Invalid team ID {}; must be between {} and {}".format(
                    team_id, 
                    MIN_TEAM_ID, 
                    MAX_TEAM_ID
                )
            )

        self.id = team_id
        self.player_name = player_name
        self.inactive_players = []

    def replace_active_player(self, new_player_name):
        """
        Replaces the active player name

        :param new_player_name: new player name
        :type new_player_name: string
        """

        # error check
        if type(new_player_name) != str:
            raise ValueError(
                "New player name {} is not str ({})".format(
                    new_player_name,
                    type(new_player_name)
                )
            )

        self.inactive_players.insert(0, self.player_name)
        self.player_name = new_player_name

    def __str__(self):
        """
        To string function

        :return: string representing this object
        """
        return_val = "Team #{:02}: {}".format(self.id, self.player_name)

        if len(self.inactive_players) > 0:
            return_val += "\n\tPrevious players: {}".format(", ".join(self.inactive_players))

        return return_val

    def __eq__(self, other_team):
        """
        Equality operator

        :param other_team: other team to compare
        :type other_team: Team object
        :return: True if the objects are equal
        """
        return self.id == other_team.id and \
            self.player_name == other_team.player_name and \
            self.inactive_players == other_team.inactive_players

class Matchup:
    """
    Defines a matchup between two teams
    """

    def __init__(self, team1, team2):
        """
        Constructor

        :param team1: first team in matchup
        :type team1: Team object
        :param team2: second team in matchup
        :type team2: Team object
        """
        if team1 == team2:
            raise ValueError("Can't create matchup between same teams!")

        # order by team ID
        if team1.id < team2.id:
            self.team1 = team1
            self.team2 = team2

        else:
            self.team1 = team2
            self.team2 = team1

    def __str__(self):
        """
        To string function

        :return: string representing this object
        """
        return "{} vs {}".format(self.team1.player_name, self.team2.player_name)

    def __eq__(self, other_matchup):
        """
        Equality operator

        :param other_matchup: other matchup to compare
        :type other_matchup: Matchup object
        :return: True if the objects are equal
        """
        return self.team1 == other_matchup.team1 and \
            self.team2 == other_matchup.team2

def create_league():
    """
    Creates league info

    :return: list of Team objects
    """

    # initial teams - inaugural season 2025
    all_teams = [
        Team(1, "Eric Schuler"),
        Team(2, "Emily Flint"),
        Team(3, "Brian Schuler"),
        Team(4, "Karen Flint"),
        Team(5, "Steve Decker"),
        Team(6, "Christopher Flint"),
        Team(7, "Carrie Flint"),
        Team(8, "Alec Hawkins"),
        Team(9, "Matt Doughty"),
        Team(10, "Dave Flint"),
        Team(11, "Ethan Denninger"),
        Team(12, "Ben Bemis"),
    ]

    # team update 2026 season
    all_teams[7].replace_active_player("Janine Flint")

    return all_teams

def remove_2025_matchups(all_matchups):
    return_val = []

    ############################################################################
    # manually created extra matchups for the 2025 season
    ############################################################################
    matchups_2025 = [

        # week 12
        # Carrie vs. Eric
        Matchup(all_teams[0], all_teams[6]),
        # Karen vs. Emily
        Matchup(all_teams[1], all_teams[3]),
        # Matt vs. Brian
        Matchup(all_teams[2], all_teams[8]),
        # Ethan vs. Steve
        Matchup(all_teams[4], all_teams[10]),
        # Christopher vs. Alec
        Matchup(all_teams[5], all_teams[7]),
        # Ben vs. Dave
        Matchup(all_teams[9], all_teams[11]),

        # week 13
        # Christopher vs. Eric
        Matchup(all_teams[0], all_teams[5]),
        # Emily vs. Ben
        Matchup(all_teams[1], all_teams[11]),
        # Steve vs. Brian
        Matchup(all_teams[2], all_teams[4]),
        # Matt vs. Karen
        Matchup(all_teams[3], all_teams[8]),
        # Ethan vs. Carrie
        Matchup(all_teams[6], all_teams[10]),
        # Dave vs. Alec
        Matchup(all_teams[7], all_teams[9]),

        # week 14
        # Emily vs. Eric
        Matchup(all_teams[0], all_teams[1]),
        # Christopher vs. Brian
        Matchup(all_teams[2], all_teams[5]),
        # Alec vs. Karen
        Matchup(all_teams[3], all_teams[7]),
        # Steve vs. Carrie
        Matchup(all_teams[4], all_teams[6]),
        # Ben vs. Matt
        Matchup(all_teams[8], all_teams[11]),
        # Ethan vs. Dave
        Matchup(all_teams[9], all_teams[10]),
    ]

    ############################################################################
   
    for m in all_matchups:
        if m not in matchups_2025:
            return_val.append(m)

    return return_val

def generate_all_matchups(all_teams):

    matchups = []

    for i in range(len(all_teams)):
        for j in range(i + 1, len(all_teams)):
            matchups.append(Matchup(all_teams[i], all_teams[j]))

    return matchups

if __name__ == "__main__":
    print()

    all_teams = create_league()

    for t in all_teams:
        print(t)

    print()

    all_matchups = generate_all_matchups(all_teams)

    # get all possible matchups over 4 years
    print("All matchups 2025-2028:")
    for m in all_matchups:
        print(m)
    print("# matchups: {}\n".format(len(all_matchups)))

    all_matchups_2026_2028 = remove_2025_matchups(all_matchups)

    # shuffle matchups
    for i in range(100):
        random.shuffle(all_matchups_2026_2028)

    print("All matchups 2026-2028:")
    for m in all_matchups_2026_2028:
        print(m)
    print("# matchups: {}\n".format(len(all_matchups_2026_2028)))

