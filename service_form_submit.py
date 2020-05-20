import time
from time import sleep
from form_one import FormOne
from form_two import FormTwo
from constants import Constants

from api import req
from proxy_handler import Proxy,ProxyHandler
from helpers import prttime

# Recap Background Service
proxyHandler = ProxyHandler()
print('[{}] Starting FORM_SUBMIT_SERVICE. Total proxies = {}'.format(prttime(),proxyHandler.total_proxies))


while True:
	# Start by Fetching Instagram Accounts
	appeal_info = req('get_form_submit_service')
	#exit(json.dumps(appeal_info))
	
	if not appeal_info:
		print(f"[{prttime()}] No appeal info found, sleeping 10 seconds")
		sleep(10)
	
	else:
		proxy = proxyHandler.getProxy()
		if proxy:
			print(f"[{appeal_info['instagram_account']['username']}] Submitting appeal with proxy {proxy.ip}:{proxy.port}...")
		else:
			print(f"[{appeal_info['instagram_account']['username']}] Submitting appeal without proxy...")
		
  
		result = None
		if appeal_info['appeal_form']['python_name'] == "form_two":
			result = FormTwo().submit(
				appeal_info['instagram_account']['username'], 
				appeal_info['appeal_resource']['full_name'],
				appeal_info['appeal_resource']['email'],
    			appeal_info['appeal_resource']['phone_number'],
       			appeal_info['spintax'],
				proxy
			)
		else:
			result = FormOne().submit(
				appeal_info['instagram_account']['username'], 
				appeal_info['appeal_resource']['full_name'],
				appeal_info['appeal_resource']['email'],
				proxy
			)
		# result = 'is_active'
		if result == True:
			# Form has been submitted, give feedback to the server
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'form_submitted',
				'form_id': appeal_info['appeal_form']['id']
			})
			print(
				f"[{prttime()}] {appeal_info['instagram_account']['username']} / Form submitted SUCCESSFULLY")
		elif result == 'is_active':
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'is_active',
    			'form_id': appeal_info['appeal_form']['id']
			})
			print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} is ALREADY ACTIVE")
		elif result == 'is_inexistent':
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'is_inexistent',
    			'form_id': appeal_info['appeal_form']['id']
			})
			print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} is INEXISTENT")
		else:
			req('register_appeal_status', data={
				'appeal_process_id': appeal_info['id'],
				'status': 'unknown',
    			'form_id': appeal_info['appeal_form']['id']
			})
			print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} Failed submitting form")
		if not proxy:
			print ('Sleeping 60 seconds because no proxy is avaialble.')
			sleep(60) 	
		else:
			sleep(5)
	



