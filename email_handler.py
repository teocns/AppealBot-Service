import pprint
import email
import poplib
import re

import time
import datetime
import calendar


from database import Database
from email.header import decode_header
from constants import Constants

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHandler:

	@staticmethod
	def getEmail():
		# Get email that has never been used, or hasn't been used for more than 15 days
		with Database.instance().cursor() as cur:
			query = """ SELECT ae.* FROM appeal_emails ae
						left join appeal_form_submits afs on ae.id = afs.email_id
						where
							ae.is_bad = 0 and
							afs.id is null or
							(afs.last_status = %s or afs.last_status = %s)
						limit 1
					"""
			cur.execute(query, (Constants.APPEAL_STATUS_REJECTED,
								Constants.APPEAL_STATUS_UNBANNED))
			return cur.fetchone()

	@staticmethod
	def log(email, text):
		with Database.instance().cursor() as cursor:
			cursor.execute('INSERT INTO appeal_emails_log VALUES(%s,%s,%s)', (
				int(time.time()), email, text
			)
			)


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


