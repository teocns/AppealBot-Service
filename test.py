import requests
import api


 current_email_data = {
            'appeal_process_id':  data['id'],
            'time_fetched': int(time.time()),
            'time_received':email['timestamp'],
            'body': str(email['body']),
            'status': email['status'],
            'message_id': email['message_id'],
            'from': str(email['from']),
            'code': email['code'],
            'subject': str(email['subject']),
            'email_id':data['email_id']
        }
print(f"[{prttime()}] Requesting to store email ({email['status']}) for {data['ig_account_username']}")
result = req('register_email_received',data = current_email_data)