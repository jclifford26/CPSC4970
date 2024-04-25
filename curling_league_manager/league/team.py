from curling_league_manager.league.identified_object import IdentifiedObject
from typing import List

from curling_league_manager.league.team_member import TeamMember


class Team(IdentifiedObject):

    def __init__(self, oid: int, name: str):
        super().__init__(oid)
        self.name = name
        self.members: List[TeamMember] = []

    def add_member(self, member: TeamMember):
        if member is not None:
            if member in self.members:
                raise ValueError("Member is already in the team.")
            elif member.email and any(m.email.upper() == member.email.upper() for m in self.members):
                raise ValueError("Member has a duplicate email address.")
            else:
                self.members.append(member)

    def member_named(self, name: str) -> TeamMember:
        for member in self.members:
            if member.name == name:
                return member
        return None

    def remove_member(self, member: TeamMember):
        if member in self.members:
            self.members.remove(member)

    def send_email(self, emailer, subject, message):
        recipients = [member.email for member in self.members if member.email]
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        return f"{self.name}: {len(self.members)} members"
