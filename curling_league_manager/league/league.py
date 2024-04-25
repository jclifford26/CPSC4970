from curling_league_manager.league.identified_object import IdentifiedObject, DuplicateOid


class League(IdentifiedObject):

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        if team is not None:
            if team.oid in {t.oid for t in self.teams}:
                raise DuplicateOid(f"The oid is duplicated when adding team {team}")
            else:
                self.teams.append(team)

    def remove_team(self, team):
        if self.competitions:
            for c in self.competitions:
                if team in c.teams_competing:
                    raise ValueError(f"This team {team} is in this league's competition.")
        if team in self.teams:
            self.teams.remove(team)

    def team_named(self, team_name):
        teams_dict = {team.name: team for team in self.teams}
        return teams_dict.get(team_name)

    def add_competition(self, competition):
        if competition is not None:
            if competition.oid in {c.oid for c in self.competitions}:
                raise DuplicateOid(f"The oid is duplicated when adding competition {competition}")
            else:
                self.competitions.append(competition)

    # Other methods remain unchanged

    def __str__(self):
        return f"{self.name}: {len(self.teams)} teams, {len(self.competitions)} competitions"
