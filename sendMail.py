import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from os.path import join, dirname
from dotenv import load_dotenv


class SendMail:
    from_address = ''
    password = ''
    file = None
    msg = None

    def __init__(self, to_address, subject='New Message', body='Message Body'):
        # Create .env file path.
        dotenv_path = join(dirname(__file__), '.env')

        # Load file from the path.
        load_dotenv(dotenv_path)

        self.password = os.getenv('GOOGLE_PASSWORD')
        self.from_address = os.getenv('GOOGLE_FROM')
        msg = MIMEMultipart()
        self.to_address = to_address
        msg['From'] = self.from_address
        msg['Subject'] = subject
        msg['To'] = self.to_address
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        self.msg = msg

    def set_recipient(self, to_address):
        self.msg['To'] = to_address
        self.to_address = to_address
        return self

    def add_attachment(self, file_path):
        # open the file to be sent
        filename = os.path.basename(file_path)
        attachment = open(file_path, "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        self.msg.attach(p)
        return self

    def send_mail(self):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.from_address, self.password)
        text = self.msg.as_string()
        s.sendmail(self.from_address, self.to_address, text)
        s.quit()

