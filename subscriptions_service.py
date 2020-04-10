from api import req
from time import sleep
from helpers import prttime
while True:
	sleep(1)

	data = req('subscription_service')
	if data and 'message' in data:
		print(f'[{prttime()}] ' + data['message'])
	else:
		print(f'[{prttime()}] No accounts found')
		sleep(30)
