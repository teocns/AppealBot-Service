import time
import base64
import os
from io import BytesIO
from time import sleep
from time import gmtime, strftime
# LOCAL LIBS

from image_generator import generate
from constants import Constants
import urllib
from email_handler import EmailHandler
from helpers import prttime, adjustJPEGRotation


from api import req

SLASH = str( '\\' if os.name == 'nt' else '/' )
while True:

    afs = req('get_for_email_submit_service')
    # afs = {
    #     'selfie_cdn_resource_filename':'565c89fbaea063211a2b621efe1a887b64056526.jpeg',
    #     'ig_account_username':'thesneakr.net',
    #     'selfie_coordinates':'136-256-272-256-272-295-136-295',
    #     'code':'',
    #     'full_name':'',
    #     'must_send_attachment':True
    # }
    if not afs:
        print(
            f"[{prttime()}] No accounts found to send appeal email. Sleeping 60 seconds")
        sleep(60)

    else:
        # Found account that requires email submit. Collect the email with the code

        
        
        selfie_processed_base64_binary = None
        
        if afs['must_send_attachment']:    
            print(f"[{prttime()}] Generating Image For ({afs['ig_account_username']})...")
            download_url = "https://cdn.appealbot.net/"+afs['selfie_cdn_resource_filename']
            import requests
            response = requests.get(
                download_url
            )
            vanilla_selfie_buffer = BytesIO(response.content)
            
            #vanilla_selfie_base64 = base64.b64encode(vanilla_selfie_buffer.getvalue())
            from PIL import Image
            img =  adjustJPEGRotation( Image.open( vanilla_selfie_buffer ) )       
            
            
            selfie_processed_base64_binary = generate(
                afs['code'], afs['full_name'], afs['ig_account_username'], afs['selfie_coordinates'],  img)
    
            #exit('ok')
            
            if not selfie_processed_base64_binary:
                raise Exception('Could not generate image')

        print(f"[{prttime()}] Sending Email For ({afs['ig_account_username']})...")
        # Send the email
        try:
            # Calculate smtp server based on pop server
            pop_serv = afs['pop_server']
            smtp_serv = "smtp."+".".join(str(pop_serv).split('.')[1:])
            
            result = EmailHandler.submitEmail(
                smtp_serv,
                afs['email'],
                afs['email_password'],
                afs['subject'],
                afs['from'],
                afs['message_id'],
                afs['message_to_send'],
                selfie_processed_base64_binary,
                afs['selfie_cdn_resource_filename'] if selfie_processed_base64_binary is not None else None
            )
            if result == False:
                print('Email error')
                result = req('handle_email_login_error', data = {
                    'email_id':afs['email_id']
                })
            else:
                req('register_sent_email', data={
                    'appeal_process_id': afs['id'],
                    'reply_to': afs['message_id'],
                    'is_error': False,
                    'base64':selfie_processed_base64_binary.decode('utf-8') if selfie_processed_base64_binary else None,
                    'body':afs['message_to_send']
                })
        except Exception as ex:
            print('[{prttime()}] -ERROR - Failed submitting email.')
            print(ex)
            req('register_sent_email', data={
                'appeal_process_id': afs['id'],
                'reply_to': afs['message_id'],
                'is_error': True,
                'base64':selfie_processed_base64_binary,
                'body':afs['message_to_send']
            })
        # delete generated image
        print(
            f"[{prttime()}] Email Submitted ({afs['ig_account_username']}) for AppealID {afs['id']}")
