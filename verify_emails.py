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

    def __init__(self, email_ru, password, pop_server):

        SRV = pop_server
        PORT = 995

        USER = email_ru
        PASSWORD = password

        mail_box = poplib.POP3_SSL(SRV, PORT)

        mail_box.user(USER)
        mail_box.pass_(PASSWORD)
        num_messages = None

        num_messages = None

        num_messages = len(mail_box.list()[1])
        mail_box.quit()


while True:
    data = req('email_verification_fetch')
    
    if data:
        try:
            print(f"[{prttime()}] Verifying "+data['email'])
            pwd = data['password']
            pop_server = data['pop_server']
            pop3handler(data['email'], pwd, pop_server)
            req('email_verification_feedback',{
                    'email_id': data['id'],
                    'resolved': True
			})
        except:
            req('email_verification_feedback',{
                    'email_id': data['id'],
                    'resolved': False
			})
    sleep(10)
