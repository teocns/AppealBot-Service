import pprint
import email
import poplib
import re
import time
import datetime
import calendar

from email.header import decode_header
from constants import Constants

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class pop3handler:
    
    def __init__(self, server, email_origin, password, handleEmail,loginErrorCallback):
    
    
        SRV = server
        PORT = 995
        
        parts = server.split(':')
        if len(parts) == 2:
            SRV = parts[0]
            PORT = parts[1]
        
        USER = email_origin
        PASSWORD = password

        mail_box = poplib.POP3_SSL(SRV, PORT)
        
        try:
            mail_box.user(USER)
            mail_box.pass_(PASSWORD)
        except Exception as ex:
            raise ex
            loginErrorCallback()
            return
        num_messages = None

        num_messages = len(mail_box.list()[1])

        email_response_status = 0

        fb_email_found = False

        emails_found = []

        for i in range(num_messages):
            try:
                raw_email = b"\n".join(mail_box.retr(i+1)[1])
                parsed_email = email.message_from_bytes(raw_email)

                e_subject = decode_header(parsed_email['Subject'])
                e_from = decode_header(parsed_email['From'])
                
                
                if e_from[0][1] != None:
                    from_output = e_from[0][0].decode(e_from[0][1])
                else:
                    from_output = e_from[0][0]
            
                if not 'facebook' in from_output:
                    #print ('Deleting non-facebook email')
                    #mail_box.dele(i+1)
                    print(f'Skipping {from_output}')
                    continue
                
                e_to = decode_header(parsed_email['To'])
                e_date = decode_header(parsed_email['Date'])
                e_id = decode_header(parsed_email['Message-ID'])[0][0]
                subject_output = ""
                # Mon, 5 Nov 2018 07:47:15 -0800
                # end_date = e_date[0][0].split(" ")[0]
                edate = e_date[0][0]
                if '(' in edate:
                    edate = edate.split(" ")
                    edate.pop()
                    edate = " ".join(edate)

                #d = ciso8601.parse_datetime(e_date[0][0])
                d = datetime.datetime.strptime(
                    edate, "%a, %d %b %Y %H:%M:%S %z")
                
                e_timestamp = calendar.timegm(d.utctimetuple())
                #print(e_timestamp)
                if e_subject[0][1] != None:
                    subject_output = e_subject[0][0].decode(e_subject[0][1])
                else:
                    subject_output = e_subject[0][0]

                

                # print(e_date[0][0])
                # print(e_timestamp)
                # print(e_id)
                
                # print(from_output)
                e_body = ''
                
                if parsed_email.is_multipart():
                    pass
                    # for payload in parsed_email.get_payload():
                    # 	if payload.is_multipart():
                    # 		print('MULTIPAYLOAD ---------------')
                    # 		print(payload.get_payload(decode=True))
                
                e_body = parsed_email.get_payload(decode=True)
                
                try:
                    if b'\n>>' in e_body:
                        e_body = e_body.split(b'\n>>')[0]
                except:
                    pass
                # print(e_body)
                
                flag = 0
                code = None
                email_response_status = 0
                
                for key, value in Constants.EMAIL_RESPONSE_STATUSES.items():
                    for n in value:
                        if n in e_body:
                            email_response_status = str(key)
                            if email_response_status == Constants.APPEAL_STATUS_VERIFICATION_CODE_RECEIVED:
                                code = re.findall(b"\d{5,}", e_body)[0]
                                flag = 1
                                break
                    if flag:
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
            except Exception as ex:
                #raise ex
                continue
        mail_box.quit()
