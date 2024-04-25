from curling_league_manager.league.identified_object import IdentifiedObject
import datetime as dt


class Competition(IdentifiedObject):

    def __init__(self, oid, teams, location, datetime=None):
        super().__init__(oid)
        self._teams_competing = teams
        self.location = location
        self.date_time = datetime if isinstance(datetime, dt.datetime) else None

    @property
    def teams_competing(self):
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        recipients = set()
        for team in self.teams_competing:
            recipients.update(member.email for member in team.members)
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        if self.date_time:
            formatted_date_time = self.date_time.strftime('%m/%d/%Y %H:%M')
            return f"Competition at {self.location} on {formatted_date_time} with {len(self.teams_competing)} teams"
        else:
            return f"Competition at {self.location} with {len(self.teams_competing)} teams"
