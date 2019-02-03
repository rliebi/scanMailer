#!/usr/bin/env python
# coding=utf-8

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
    cc = []
    recipients = []

    def __init__(self, to_address, subject='New Message', body='Message Body'):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        msg = MIMEMultipart()

        self.recipients = []
        self.cc = []
        self.password = os.getenv('GOOGLE_PASSWORD')
        self.from_address = os.getenv('GOOGLE_FROM')
        self.to_address = to_address
        self.recipients.append(to_address)
        msg['From'] = self.from_address
        msg['Subject'] = subject
        msg['To'] = self.to_address
        msg.attach(MIMEText(body, 'plain', "utf-8"))
        self.msg = msg

    def set_cc(self, cc):
        self.cc = cc
        self.msg['Cc'] = ', '.join(cc)
        self.recipients += cc

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
        s.sendmail(self.from_address, self.recipients, text)
        s.quit()


