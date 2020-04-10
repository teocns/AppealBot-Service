import json
import requests
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


class pop3handler:

	def __init__(self, email_ru, password):

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


while True:
	data = requests.get(
		url='http://appealbot.net/admin/verify-appeal-emails'
	).text

	if data:
		email = json.loads(data)
		try:
			print(f"Verifying {email['email']}")
			pwd = email['password']
			pop3handler(email['email'], pwd)
			txt = 'OK'
			print(txt)
			requests.post(
				url='http://appealbot.net/admin/verify-appeal-emails',
				data={
					'email': email['email'],
					'is_bad': 0
				}
			)
		except:
			requests.post(
				url='http://appealbot.net/admin/verify-appeal-emails',
				data={
					'email': email['email'],
					'is_bad': 1
				}
			)
			print('ERROR')
