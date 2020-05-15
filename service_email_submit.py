import time
import base64
import os

from time import sleep
from time import gmtime, strftime

# LOCAL LIBS

from image_generator import ImageGenerator
from constants import Constants

from email_handler import EmailHandler
from helpers import prttime


from api import req


while True:

	afs = req('get_for_email_submit_service')
	
	if not afs:
		print(
			f"[{prttime()}] No accounts found to send appeal email. Sleeping 60 seconds")
		sleep(60)

	else:
		# Found account that requires email submit. Collect the email with the code

		print(f"[{prttime()}] Generating Image For ({afs['ig_account_username']})...")
		# try:

		# Get base 64 image string to store it into the database
		filename = ImageGenerator.generate(
			afs['code'], afs['full_name'], afs['ig_account_username'])

		if not filename:
			raise Exception('Could not generate image')

		print(f"[{prttime()}] Sending Email For ({afs['ig_account_username']})...")

		# Send the email
		try:
			EmailHandler.submitEmail(
				afs['email'],
				afs['email_password'],
				afs['subject'],
				afs['from'],
				afs['message_id'],
				None,
				filename
			)
			req('register_sent_email', data={
				'appeal_process_id': afs['id'],
				'reply_to': afs['message_id'],
				'is_error': False,
				'filename':filename
			})
		except:
			print('[{prttime()}] -ERROR - Failed submitting email.')
			req('register_sent_email', data={
				'appeal_process_id': afs['id'],
				'reply_to': afs['message_id'],
				'is_error': True,
				'filename':filename
			})

		# delete generated image

		

		print(
			f"[{prttime()}] Email Submitted ({afs['ig_account_username']}) for AppealID {afs['id']}")
