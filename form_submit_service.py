import time
from time import sleep
from form_one import FormOne
from constants import Constants

from api import req
from proxy_handler import Proxy,ProxyHandler

# Recap Background Service
proxyHandler = ProxyHandler()
print('Starting FORM_SUBMIT_SERVICE. Total proxies = {}'.format(proxyHandler.total_proxies))

while True:
	# Start by Fetching Instagram Accounts
	appeal_info = req('get_appeal_process')


	if not appeal_info:
		print("No appeal info found, sleeping 10 seconds")
		sleep(10)
	
	else:
		proxy = proxyHandler.getProxy()
		if proxy:
			print(f"[{appeal_info['ig_account_username']}] Submitting appeal with proxy {proxy.ip}:{proxy.port}...")
		else:
			print(f"[{appeal_info['ig_account_username']}] Submitting appeal without proxy...")
		# Send FORM ONE
		result = FormOne().submit(
			appeal_info['ig_account_username'], 
   			appeal_info['full_name'],
      		appeal_info['email'],
			proxy
        )
		# result = 'is_active'
		if result == True:
			# Form has been submitted, give feedback to the server
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'form_submitted'
			})
			print(
				f"[{appeal_info['ig_account_username']}] Form submitted SUCCESSFULLY")
		elif result == 'is_active':
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'is_already_active'
			})
			print(f"[{appeal_info['ig_account_username']}] is ALREADY ACTIVE")
		elif result == 'is_inexistent':
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'is_inexistent'
			})
			print(f"[{appeal_info['ig_account_username']}] is INEXISTENT")
		else:
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'unknown'
			})
			print(f"[{appeal_info['ig_account_username']}] Failed submitting form")
		if not proxy:
			print ('Sleeping 60 seconds because no proxy is avaialble.')
			sleep(60) 
	



