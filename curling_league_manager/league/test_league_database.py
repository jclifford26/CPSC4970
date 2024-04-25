import unittest
from league_database import LeagueDatabase
from curling_league_manager.league.league import League


class TestLeagueDatabase(unittest.TestCase):
    def setUp(self):
        self.db = LeagueDatabase.instance()
        if not self.db:
            self.db = LeagueDatabase()
            LeagueDatabase._sole_instance = self.db

    def tearDown(self):
        self.db = None

    def test_import_league_teams(self):
        league = League(1, "Big League")
        self.db.add_league(league)

        # Create a temporary CSV file for testing
        with open("test_teams.csv", "w") as file:
            file.write("Big League\n")
            file.write("Team Bedrock, Fred, Fred@Flinstone.com\n")
            file.write("Team Rock Vegas, Barney, Barney@Rubble.com\n")

        # Import teams from the temporary CSV file
        self.db.import_league_teams(league, "test_teams.csv")

        # Check if teams and members were imported correctly
        self.assertEqual(len(league.teams), 2)
        self.assertEqual(len(league.teams[0].members), 1)
        self.assertEqual(len(league.teams[1].members), 1)

        # Clean up the temporary CSV file
        # os.remove("test_teams.csv")


if __name__ == '__main__':
    unittest.main()
