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
import requests

from api import req


while True:
	sleep(60) # Minimum delay to avoid getting pwned by Instagram
	print ('[60 seconds delay]')
	afs = req('get_for_unban_checker_service')

	if (afs):
		print(f"Checking {afs['username']}..")
		username = afs['username']
		response = requests.get(
			url=f'https://www.instagram.com/{username}/?__a=1',
			headers={
				'cookie': 'ig_cb=1; mid=W_qWaAALAAEZPRg-l9ov00RtASU1; mcd=3; ig_did=1DFFC321-3E88-40EC-8C22-42F022623861; fbm_124024574287414=base_domain=.instagram.com; datr=2Rk-XtVLeBQiJ2iISbSkwaaB; csrftoken=80GnQQTkw7AwZVLFg8C5fAtwIOPV41Qx; ds_user_id=2260813760; sessionid=2260813760%3AVEH4dUdINEDP3U%3A19; shbid=10885; shbts=1585482138.4205203; rur=FRC; urlgen="{\"79.13.108.24\": 3269}:1jIWKw:EirFmFFJnY7TzjJvDpXsgPh496Y"',
				'host': 'www.instagram.com',
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
			}
		)

		if response.status_code == 200 and response.text != "{}":
			print(f'[{username}] Is active, confirming unban')
		
			req(
				'register_unban_confirmation',
				{
					'ig_account_id': afs['id']
				}
			)
	else:
		print('Found no accounts..')
