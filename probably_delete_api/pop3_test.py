#!/usr/bin/env python
import pprint
import email
import poplib
import re

import time
import datetime
import calendar

from email.header import decode_header


import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('host')
args = parser.parse_args()


def pop3_test(email_ru, password):
	try:
		SRV = "pop.mail.ru"
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
		return '{"resolved":true}'
	except:
		return '{"resolved":false}'

print ( pop3_test(args.email,args.password) )