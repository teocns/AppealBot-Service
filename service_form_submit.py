import time
from time import sleep
from form_one import submit_form_one
from form_two import submit_form_two
from constants import Constants

from api import req
from proxy_handler import Proxy,ProxyHandler
from helpers import prttime


proxyHandler = ProxyHandler()
print('[{}] Starting FORM_SUBMIT_SERVICE. Total proxies = {}'.format(prttime(),proxyHandler.total_proxies))


while True:
    # Start by Fetching Instagram Accounts
    appeal_info = req('get_form_submit_service')
    
    #exit(json.dumps(appeal_info))
    try:    
        if not appeal_info:
            print(f"[{prttime()}] No appeal info found, sleeping 10 seconds")
            sleep(10)
        
        else:
            if appeal_info and appeal_info['previous_status'] == 0 or appeal_info['previous_status'] == '0':
                print("ALERT\nALERT\nALERT\nALERT")
            proxy = proxyHandler.getProxy()
            if proxy:
                print(f"[{appeal_info['instagram_account']['username']}] Submitting {appeal_info['appeal_form']['python_name']} with proxy {proxy.ip}:{proxy.port} [AP {appeal_info['id']}]")
            else:
                print(f"[{appeal_info['instagram_account']['username']}] Submitting {appeal_info['appeal_form']['python_name']} without proxy...")
            
    
            result = None
            if appeal_info['appeal_form']['python_name'] == "form_two":
                result = submit_form_two(
                    appeal_info['instagram_account']['username'], 
                    appeal_info['appeal_resource']['full_name'],
                    appeal_info['appeal_resource']['email'],
                    appeal_info['appeal_resource']['phone_number'],
                    appeal_info['spintax'],
                    proxy
                )
            else:
                result = submit_form_one(
                    appeal_info['instagram_account']['username'], 
                    appeal_info['appeal_resource']['full_name'],
                    appeal_info['appeal_resource']['email'],
                    proxy
                )

            if result == True:
                # Form has been submitted, give feedback to the server
                req('callback_form_submit_service', data={
                    'appeal_process_id': appeal_info['id'],
                    'status': 'form_submitted',
                    'form_id': appeal_info['appeal_form']['id']
                })
                print(
                    f"[{prttime()}] {appeal_info['instagram_account']['username']} / Form submitted SUCCESSFULLY")
            elif result == 'is_active':
                req('callback_form_submit_service', data={
                    'appeal_process_id': appeal_info['id'],
                    'status': 'is_active',
                    'form_id': appeal_info['appeal_form']['id']
                })
                print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} is ALREADY ACTIVE")
            elif result == 'is_inexistent':
                req('callback_form_submit_service', data={
                    'appeal_process_id': appeal_info['id'],
                    'status': 'is_inexistent',
                    'form_id': appeal_info['appeal_form']['id']
                })
                print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} LOGIN FOR REVIEW")
            elif result == "login_for_review":
                req('callback_form_submit_service', data={
                    'appeal_process_id': appeal_info['id'],
                    'status': 'login_for_review',
                    'form_id': appeal_info['appeal_form']['id']
                })
                print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} USER LOGIN REQUIRED FOR REVIEW")
            elif result == "confirm_its_you":
                req('callback_form_submit_service', data={
                    'appeal_process_id': appeal_info['id'],
                    'status': 'confirm_its_you',
                    'form_id': appeal_info['appeal_form']['id']
                })
                print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} is INEXISTENT")
            else:
                req('callback_form_submit_service', data={
                    'appeal_process_id': appeal_info['id'],
                    'status': 'unknown',
                    'form_id': appeal_info['appeal_form']['id']
                })
                print(f"[{prttime()}] / {appeal_info['instagram_account']['username']} Failed submitting form")
            if not proxy:
                print ('Sleeping 180 seconds because no proxy is available. Preventing eventual IP blocks.')
                sleep(60)
    except Exception as ex:
        print('Exception occured:\n'+str(ex))



