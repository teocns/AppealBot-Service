#!/usr/local/bin/python3.8
import json
import requests
import pprint
import email
import poplib
import re
from time import sleep
import time
import datetime
import calendar
from api import req

from email.header import decode_header


import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from helpers import prttime

class pop3handler:

    def __init__(self, email_ru, password,pop_server ):

        SRV = pop_server
        PORT = 995
        
        
        parts = pop_server.split(':')
        if len(parts) == 2:
            SRV = parts[0]
            PORT = parts[1]

        USER = email_ru
        PASSWORD = password

        mail_box = poplib.POP3_SSL(SRV, PORT)

        mail_box.user(USER)
        mail_box.pass_(PASSWORD)
        num_messages = None

        num_messages = None

        num_messages = len(mail_box.list()[1])
        mail_box.quit()

class smtphandler:
    def __init__(self,email_sender,password,smtp_server):
        parts = smtp_server.split(':')
        connection = None
        if len(parts) == 2:
            connection = smtplib.SMTP_SSL(parts[0],parts[1])
        else:
            connection = smtplib.SMTP_SSL(smtp_server,465)
        connection.login(email_sender, password)
        connection.quit()
    
while True:
    
    data = req('email_verification_fetch')
    
    if data:
        try:
            print(f"[{prttime()}] Verifying "+data['email'])
            pwd = data['password']
            pop_server = data['pop_server']
            smtp_server = data['smtp_server']
            
            pop3handler(data['email'], pwd, pop_server)
            smtphandler(data['email'], pwd, smtp_server)
            req('email_verification_feedback',{
                    'email_id': data['id'],
                    'resolved': True
			})
            print('OK')
        except Exception as ex:
            req('email_verification_feedback',{
                    'email_id': data['id'],
                    'resolved': False
			})
            print (ex)
    else:
        print ('No emails to verify found')
        sleep(10)
    sleep(3)
