

import time 
from time import sleep
from email_handler import EmailHandler
import codecs
from constants import Constants
import simplejson as json
import pprint
from api import req
from pop3handler import pop3handler
last_id_fetched = 0 # useful to skip last id on next iterations
from helpers import prttime

while True:
    try:
        data = req('get_for_reading_service')
        
        try:
            a = data['email']
        except:
            sleep(5)
            print(f'[{prttime()}] No email awaiting to be readed')
            continue
        
        # This status is in FORM SUBMITTED status and seeks for email read. Let's search for the email sent by Facebook
        print (f"[{prttime()}] Checking emails for {data['ig_account_username']} / {data['email']} (SENDER AP {data['id']})")
        
        
        
        def handleFbEmailFound(mail_box,email):
            
            current_email_data = {
                'appeal_process_id':  data['id'],
                'time_fetched': int(time.time()),
                'time_received':email['timestamp'],
                'body': email['body'].decode('utf-8'),
                'status': email['status'],
                'message_id': email['message_id'],
                'from': str(email['from']),
                'code': email['code'],
                'subject': str(email['subject']),
                'email_id':data['email_id']
            }
            print(f"[{prttime()}] Requesting to store email ({email['status']}) for {data['ig_account_username']}")
            result = req('register_email_received',data = current_email_data)
            if result['delete_email']:
                print (result['message'])
        def handleLoginErrorCallback():
            result = req('handle_email_login_error', data = {
                'email_id':data['email_id']
            })
            
        pop3handler(data['pop_server'],data['email'],data['email_password'],handleFbEmailFound,loginErrorCallback=handleLoginErrorCallback)
    except Exception as ex:
        print(f'[{prttime()}] Exception occured - Skipping')
        print(ex)


    