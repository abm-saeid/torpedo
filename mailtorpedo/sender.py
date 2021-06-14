from os.path import exists
import json
import smtplib
from .binder import Binder

class Sender():
    def __init__(self, creds, reader, template):
        if not exists(creds):
            raise FileNotFoundError("Credential file not found.")
        else:
            with open(creds, 'r', encoding='utf-8') as credfile:
                self.credentials = json.loads(credfile.read())

        self.binder = Binder(reader, template)

    def get_server(self):
        server = smtplib.SMTP(
            host=self.credentials['HOST'], 
            port=self.credentials['PORT'],
        )
        server.starttls()
        server.login(
            user=self.credentials['USER'],
            password=self.credentials['PASSWORD']
        )

        return server
    
    def send(self):
        mail_list = list(self.binder.parse())

        if 'SENDER_EMAIL' not in self.credentials.keys():
            email = self.credentials['USER']
        else:
            email = self.credentials['SENDER_EMAIL']
        
        server = self.get_server()

        for receiver in mail_list:
            try:
                server.sendmail(email, receiver[0], receiver[1].as_string())
                print("Mail sent to", receiver[0])
            except smtplib.SMTPServerDisconnected:
                server = self.get_server()
                receiver[1]['From'] = email
                server.sendmail(email, receiver[0], receiver[1].as_string())
                print("Mail sent to", receiver[0])
        
        server.quit()