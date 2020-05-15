from api import req
from time import sleep
from helpers import prttime
while True:
	sleep(1)

	data = req('subscription_service')
	if data is not None and 'message' in data and data['message']:
		print(f'[{prttime()}] ' + str(data['message']))
	else:
		print(f'[{prttime()}] No accounts found')
		sleep(30)
