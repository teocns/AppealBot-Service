import pprint
import email
import poplib
import re

import time
import datetime
import calendar



from email.header import decode_header
from constants import Constants

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHandler:
	@staticmethod
	def submitEmail(email_from, password, email_received_subject, email_to, in_reply_to, text=None, filepath=None):
		
		email_sender = email_from
		email_receiver =  email_to.replace('>','').replace('Facebook <','')

		msg = MIMEMultipart()
		msg['From'] = email_sender
		msg['To'] = email_receiver
		#msg['To'] = email_receiver
		msg['References'] = in_reply_to
		msg['In-Reply-To'] = in_reply_to
		#msg['Bcc'] = 'arthuraxton@gmail.com'
		msg['Subject'] = 'RE: '+email_received_subject

		body = ''
		msg.attach(MIMEText(body, 'plain'))

		if filepath:
			filename = filepath
			
			attachment = open(filename, 'rb')
			part = MIMEBase('application', 'octet_stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition',
							"attachment; filename= "+filename)
			msg.attach(part)

		text = msg.as_string()

		connection = smtplib.SMTP_SSL('smtp.mail.ru:465')

		
		connection.login(email_sender, password)
		asd = connection.sendmail(email_sender, email_receiver, text)
		connection.quit()


