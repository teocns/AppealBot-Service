import requests
import json

REQUEST_ENDPOINT = "https://appealbot.net/api/backend"

def req(action,data = {}):
    
    postdata = {
        'action':action,
        'data':data
    }
    
    try:
        res = requests.post(
            url=REQUEST_ENDPOINT,
            json= postdata,
            headers={
                "Authorization":"Basic aW10aGViZXN0YnJvOjEyM0FwcGVhbGJvdCo="
            }
        )
        #print(res.text);
    except:
        print(f'Server didnt respond')
        return
    try:
        return json.loads(res.text)
    except:
        print(f'Server responded with non valid json: {res.text}')
        
def log(text):
    with open('log.txt','a') as file:
        file.write(text)