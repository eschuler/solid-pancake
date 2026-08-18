#!/usr/bin/env python3

import copy
import unittest

from create_schedule import *

class TeamTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.id1 = 1
        self.id2 = 6
        self.id3 = 12

        self.player_name1 = "Eric Schuler"
        self.player_name2 = "Panda Schuler"
        self.player_name3 = "Froggie Flint"

        self.t1 = Team(self.id1, self.player_name1)
        self.t1_copy = Team(self.id1, self.player_name1)
        self.t2 = Team(self.id2, self.player_name2)
        self.t3 = Team(self.id3, self.player_name3)
        self.t4 = Team(self.id1, self.player_name2)

    def test_init(self):

        self.assertEqual(self.t1.id, self.id1)
        self.assertEqual(self.t1_copy.id, self.id1)
        self.assertEqual(self.t2.id, self.id2)
        self.assertEqual(self.t3.id, self.id3)
        self.assertEqual(self.t4.id, self.id1)

        self.assertEqual(self.t1.player_name, self.player_name1)
        self.assertEqual(self.t1_copy.player_name, self.player_name1)
        self.assertEqual(self.t2.player_name, self.player_name2)
        self.assertEqual(self.t3.player_name, self.player_name3)
        self.assertEqual(self.t4.player_name, self.player_name2)

        # test bad inputs
        for invalid_id in [-1, 0, 13, ""]:
            with self.assertRaises(ValueError):
                #print("checking {}".format(invalid_id))
                Team(invalid_id, "")

        for invalid_player_name in ["", 42]:
            with self.assertRaises(ValueError):
                #print("checking {}".format(invalid_player_name))
                Team(1, invalid_player_name)

    def test_eq(self):
        self.assertTrue(self.t1 == self.t1)
        self.assertTrue(self.t1_copy == self.t1_copy)
        self.assertTrue(self.t1 == self.t1_copy)
        self.assertTrue(self.t1_copy == self.t1)
        self.assertTrue(self.t2 == self.t2)
        self.assertTrue(self.t3 == self.t3)
        self.assertTrue(self.t4 == self.t4)

        self.assertFalse(self.t1 == self.t2)
        self.assertFalse(self.t1 == self.t3)
        self.assertFalse(self.t1 == self.t4)
        self.assertFalse(self.t2 == self.t1)
        self.assertFalse(self.t2 == self.t3)
        self.assertFalse(self.t2 == self.t4)
        self.assertFalse(self.t3 == self.t1)
        self.assertFalse(self.t3 == self.t2)
        self.assertFalse(self.t3 == self.t4)

    def test_replace_active_player(self):
        t1_copy = copy.deepcopy(self.t1)
        t1_copy.replace_active_player("Kristen Flint")

        self.assertEqual(t1_copy.id, self.id1)
        self.assertEqual(t1_copy.player_name, "Kristen Flint")
        self.assertEqual(t1_copy.inactive_players, [self.player_name1])

class MatchupTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.id1 = 1
        self.id2 = 6
        self.id3 = 12

        self.player_name1 = "Eric Schuler"
        self.player_name2 = "Panda Schuler"
        self.player_name3 = "Froggie Flint"

        self.t1 = Team(self.id1, self.player_name1)
        self.t2 = Team(self.id2, self.player_name2)
        self.t3 = Team(self.id3, self.player_name3)

        self.m1 = Matchup(self.t1, self.t2)
        self.m2 = Matchup(self.t1, self.t3)
        self.m3 = Matchup(self.t2, self.t3)

    def test_init(self):
        self.assertEqual(self.m1.team1, self.t1)
        self.assertEqual(self.m1.team2, self.t2)
        self.assertEqual(self.m2.team1, self.t1)
        self.assertEqual(self.m2.team2, self.t3)
        self.assertEqual(self.m3.team1, self.t2)
        self.assertEqual(self.m3.team2, self.t3)

        # test invalid
        for team in [self.t1, self.t2, self.t3]:
            with self.assertRaises(ValueError):
                Matchup(team, team)
        with self.assertRaises(ValueError):
            Matchup(self.t1, copy.deepcopy(self.t1))

    def test_eq(self):
        self.assertTrue(self.m1 == self.m1)
        self.assertTrue(self.m1 == self.m1)
        self.assertTrue(self.m1 == self.m1)
        self.assertTrue(self.m1 == copy.deepcopy(self.m1))

        self.assertFalse(self.m1 == self.m2)
        self.assertFalse(self.m1 == self.m3)
        self.assertFalse(self.m2 == self.m1)
        self.assertFalse(self.m2 == self.m3)
        self.assertFalse(self.m3 == self.m1)
        self.assertFalse(self.m3 == self.m2)

if __name__ == "__main__":
    print()
    unittest.main(verbosity=2)
    print()

