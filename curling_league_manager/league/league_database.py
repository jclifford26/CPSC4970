import pickle
import os
import csv
from logging import getLogger, basicConfig, INFO
from curling_league_manager.league.team_member import TeamMember
from curling_league_manager.league.team import Team

# Configure logging
basicConfig(level=INFO)
logger = getLogger(__name__)


class LeagueDatabase:

    _sole_instance = None
    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)
        except FileNotFoundError:
            logger.error("File not found.")
        except IOError:
            logger.error("An error occurred while reading the file.")

    def __init__(self):
        self._leagues = []
        self._last_oid = 0

    @property
    def leagues(self):
        return self._leagues

    def add_league(self, league):
        self.leagues.append(league)

    def remove_league(self, league):
        self.leagues.remove(league)

    def league_named(self, name):
        return next((league for league in self.leagues if league.name == name), None)

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        backup_name = file_name + ".backup"
        try:
            if os.path.exists(file_name):
                os.rename(file_name, backup_name)
            with open(file_name, mode='wb') as f:
                pickle.dump(self, f)
        except Exception:
            logger.error("An error occurred while saving the database.")

    def import_league_teams(self, league, file_name):
        try:
            with open(file_name, newline='', encoding="utf-8") as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    team = league.team_named(row["Team name"])
                    if team is None:
                        team = Team(self.next_oid(), row["Team name"])
                        league.add_team(team)
                    team.add_member(TeamMember(self.next_oid(), row["Member name"], row["Member email"]))
            return league
        except FileNotFoundError:
            logger.error("File not found.")
        except Exception:
            logger.error("An error occurred during import.")

    def export_league_teams(self, league, file_name):
        try:
            with open(file_name, 'w', newline='', encoding="utf-8") as f:
                csv_writer = csv.DictWriter(f, fieldnames=["Team name", "Member name", "Member email"])
                csv_writer.writeheader()
                for team in league.teams:
                    for member in team.members:
                        csv_writer.writerow({"Team name": team.name, "Member name": member.name, "Member email": member.email})
        except Exception:
            logger.error("An error occurred during export.")
