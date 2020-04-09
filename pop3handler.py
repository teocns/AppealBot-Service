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

class pop3handler:
	
	def __init__(self, email_ru, password, handleEmail):
	
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

		email_response_status = 0

		fb_email_found = False

		emails_found = []

		for i in range(num_messages):

			raw_email = b"\n".join(mail_box.retr(i+1)[1])
			parsed_email = email.message_from_bytes(raw_email)

			e_subject = decode_header(parsed_email['Subject'])
			e_from = decode_header(parsed_email['From'])
			e_to = decode_header(parsed_email['To'])
			e_date = decode_header(parsed_email['Date'])
			e_id = decode_header(parsed_email['Message-ID'])[0][0]
			subject_output = ""
			# Mon, 5 Nov 2018 07:47:15 -0800
			d = datetime.datetime.strptime(
				e_date[0][0], "%a, %d %b %Y %H:%M:%S %z")
			e_timestamp = calendar.timegm(d.utctimetuple())

			if e_subject[0][1] != None:
				subject_output = e_subject[0][0].decode(e_subject[0][1])
			else:
				subject_output = e_subject[0][0]

			if e_from[0][1] != None:
				from_output = e_from[0][0].decode(e_from[0][1])
			else:
				from_output = e_from[0][0]
			
			if not 'facebook' in from_output:
				#print ('Deleting non-facebook email')
				mail_box.dele(i+1)
				continue

			# print(e_date[0][0])
			# print(e_timestamp)
			# print(e_id)
			
			# print(from_output)
			e_body = ''
			if parsed_email.is_multipart():
				pass
				for payload in parsed_email.get_payload():
					if payload.is_multipart(): ...
					print('MULTIPAYLOAD ---------------')
					print(payload.get_payload(decode=True))
					e_body = "asdd"
			else:
				e_body = parsed_email.get_payload(decode=True)

			if b'\n>>' in e_body:
				e_body = e_body.split(b'\n>>')[0]
			# print(e_body)
			
			exit = 0
			code = None
			email_response_status = 0
			for key, value in Constants.EMAIL_RESPONSE_STATUSES.items():
				for n in value:
					if n in e_body:
						email_response_status = str(key)
						if email_response_status == Constants.APPEAL_STATUS_VERIFICATION_CODE_RECEIVED:
							code = re.findall(b"\d{5,}", e_body)[0]
							exit = 1
							break
				if exit:
					break

			if not email_response_status:
				email_response_status = Constants.APPEAL_STATUS_UNKNOWN
			email_to_save = {
				'body':  e_body,
				'timestamp': int(e_timestamp),
				'subject': subject_output,
				'message_id': e_id,
				'from': from_output,
				'code': code,
				'status': email_response_status
			}

			must_skip = False
			email_to_save['index'] = i
			handleEmail(mail_box,email_to_save)
		mail_box.quit()

	