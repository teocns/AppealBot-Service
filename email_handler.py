import pprint
import email
import poplib
import re

import time
import datetime
import calendar

import urllib

from email.header import decode_header
from constants import Constants

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
SLASH = str( '\\' if os.name == 'nt' else '/' )
class EmailHandler:
    @staticmethod
    def submitEmail(smtp_server, email_from, password, email_received_subject, email_to, in_reply_to, text='', base64_binary_attachment=None, filename = None):
        email_sender = email_from
        email_receiver =  email_to.replace('>','').replace('Facebook <','')

        msg = MIMEMultipart()
        msg['From'] = email_sender
        print('Sending email from :'+email_sender)
        print ('To:'+ email_receiver)
        #msg['To'] = "mrkgmaster@gmail.com"
        msg['To'] = email_receiver
        msg['References'] = in_reply_to
        msg['In-Reply-To'] = in_reply_to
        #msg['Bcc'] = 'arthuraxton@gmail.com'
        msg['Subject'] = 'RE: '+email_received_subject

        body = text
        msg.attach(MIMEText(body, 'plain'))

        if base64_binary_attachment:
            filename = filename if filename else 'attachment.jpeg'
            part = MIMEBase('image', 'jpeg')
            part.set_payload(base64_binary_attachment.decode('utf-8'))
            part.add_header('Content-Transfer-Encoding','base64')
            part.add_header('Content-Disposition',
                            "attachment; filename= "+filename)
            msg.attach(part)

        text = msg.as_string()
        result = True
        try:
            parts = smtp_server.split(':')
            connection = None
            if len(parts) == 2:
                connection = smtplib.SMTP_SSL(parts[0],parts[1])
            else:
                connection = smtplib.SMTP_SSL(smtp_server,465)
            connection.login(email_sender, password)
            asd = connection.sendmail(email_sender, email_receiver, text)
            connection.quit()
        except Exception as ex:
            result = False
        
        connection.quit()
        return result;

