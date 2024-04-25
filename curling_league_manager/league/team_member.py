from curling_league_manager.league.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):

    def __init__(self, oid: int, name: str, email: str):
        super().__init__(oid)
        if not name:
            raise ValueError("Name cannot be empty.")
        if email is not None and not email.strip():
            raise ValueError("Email cannot be empty or whitespace.")
        self.name = name
        self.email = email

    def send_email(self, emailer, subject: str, message: str):
        if self.email:
            emailer.send_plain_email([self.email], subject, message)

    def __str__(self):
        return f"{self.name}<{self.email}>"
