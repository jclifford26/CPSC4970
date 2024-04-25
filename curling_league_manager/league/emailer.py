import yagmail

from oauth2 import GOOGLE_REFRESH_TOKEN, send_mail, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, get_authorization


class Emailer:
    _sole_instance = None
    sender_address = ""

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address

    def send_plain_email(self, recipients, subject, message):
        try:
            yagmail.SMTP(user='wareagleintexas').send(to=recipients, subject=subject, contents=message)
            print("Email sent")
        except:
            print("Error sending email")



#Test send email
if __name__ == '__main__':
    if GOOGLE_REFRESH_TOKEN is None:
        print('No refresh token found, obtaining one')
        refresh_token, access_token, expires_in = get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        print('Set the following as your GOOGLE_REFRESH_TOKEN:', refresh_token)
        exit()

    send_mail('wareagleintexas@gmail.com', 'wareagleintexas@gmail.com',
              'A mail from you from Python',
              '<b>A mail from you from Python</b><br><br>' +
              'So happy to hear from you!')